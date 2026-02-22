from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render


def logout_view(request):
    logout(request)
    return redirect("/")


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("/dashboard/")

        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm(request)

    return render(request, "accounts/login.html", {"form": form})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/dashboard/")

        messages.error(request, "Signup failed. Please correct the errors below.")
    else:
        form = UserCreationForm()

    return render(request, "accounts/signup.html", {"form": form})
