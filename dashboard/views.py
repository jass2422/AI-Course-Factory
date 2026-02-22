import json
import logging

from django.conf import settings

logger = logging.getLogger(__name__)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course, Lesson, Module, Quiz


def landing(request):
    return render(request, "dashboard/landing.html")


@login_required(login_url="/login/")
def dashboard_home(request):
    return render(request, "dashboard/home.html")


@login_required(login_url="/login/")
def generate_course(request):
    if request.method != "POST":
        return redirect("dashboard:home")

    topic = (request.POST.get("topic") or "").strip()
    level = (request.POST.get("level") or "").strip()

    allowed_levels = {"Beginner", "Intermediate", "Advanced"}
    if not topic or level not in allowed_levels:
        messages.error(request, "Please provide a topic and level.")
        return redirect("dashboard:home")

    if not getattr(settings, "GROQ_API_KEY", ""):
        messages.error(request, "GROQ_API_KEY is not configured.")
        return redirect("dashboard:home")

    try:
        from groq import Groq

        client = Groq(api_key=settings.GROQ_API_KEY)

        prompt = (
            "Generate a JSON object for a course.\n"
            "Requirements:\n"
            "- Exactly 3 modules\n"
            "- Each module has exactly 2 lessons\n"
            "- Each module has exactly 5 quiz questions\n\n"
            "Return JSON ONLY (no markdown).\n\n"
            "Schema:\n"
            "{\n"
            '  "title": string,\n'
            '  "topic": string,\n'
            '  "level": "Beginner"|"Intermediate"|"Advanced",\n'
            '  "modules": [\n'
            "    {\n"
            '      "title": string,\n'
            '      "lessons": [\n'
            "        {\n"
            '          "title": string,\n'
            '          "content": string\n'
            "        }\n"
            "      ],\n"
            '      "quiz_questions": [\n'
            "        {\n"
            '          "question": string,\n'
            '          "choices": [string, string, string, string],\n'
            '          "answer": string\n'
            "        }\n"
            "      ]\n"
            "    }\n"
            "  ]\n"
            "}\n\n"
            f"Topic: {topic}\n"
            f"Level: {level}\n"
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You generate valid JSON only.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        raw_content = response.choices[0].message.content or "{}"
        raw_json = raw_content
        if "{" in raw_content and "}" in raw_content:
            raw_json = raw_content[raw_content.find("{") : raw_content.rfind("}") + 1]

        course_data = json.loads(raw_json)
    except Exception as exc:
        error_message = f"{type(exc).__name__}: {exc}"
        print(error_message)
        logger.exception("Course generation failed: %s", error_message)

        return render(
            request,
            "dashboard/home.html",
            {
                "generation_error": error_message,
                "topic": topic,
                "level": level,
            },
        )

    modules_data = course_data.get("modules") or []
    if not isinstance(modules_data, list) or len(modules_data) != 3:
        messages.error(request, "Generated course format was invalid. Please try again.")
        return redirect("dashboard:home")

    title = (course_data.get("title") or f"{topic} ({level})").strip()[:255]

    with transaction.atomic():
        course = Course.objects.create(
            user=request.user,
            title=title,
            topic=topic,
            level=level,
        )

        for module_index, module_data in enumerate(modules_data, start=1):
            module_title = (module_data.get("title") or f"Module {module_index}").strip()[:255]
            module = Module.objects.create(
                course=course,
                title=module_title,
                order=module_index,
            )

            lessons_data = module_data.get("lessons") or []
            for lesson_index, lesson_data in enumerate(list(lessons_data)[:2], start=1):
                lesson_title = (lesson_data.get("title") or f"Lesson {lesson_index}").strip()[:255]
                lesson_content = (lesson_data.get("content") or "").strip()
                Lesson.objects.create(
                    module=module,
                    title=lesson_title,
                    content=lesson_content,
                    order=lesson_index,
                )

            quiz_questions = module_data.get("quiz_questions") or []
            Quiz.objects.create(module=module, questions=list(quiz_questions)[:5])

    return redirect("course_detail", course_id=course.id)


@login_required(login_url="/login/")
def course_detail(request, course_id: int):
    course = get_object_or_404(
        Course.objects.prefetch_related("modules__lessons", "modules__quizzes"),
        id=course_id,
        user=request.user,
    )

    lesson_id = request.GET.get("lesson")
    active_lesson = None

    if lesson_id:
        try:
            active_lesson_id = int(lesson_id)
        except (TypeError, ValueError):
            active_lesson_id = None

        if active_lesson_id:
            active_lesson = (
                Lesson.objects.select_related("module")
                .filter(id=active_lesson_id, module__course=course)
                .first()
            )

    if not active_lesson:
        active_lesson = (
            Lesson.objects.select_related("module")
            .filter(module__course=course)
            .order_by("module__order", "order")
            .first()
        )

    active_module = active_lesson.module if active_lesson else None

    return render(
        request,
        "dashboard/course_detail.html",
        {
            "course": course,
            "active_lesson": active_lesson,
            "active_module": active_module,
        },
    )
