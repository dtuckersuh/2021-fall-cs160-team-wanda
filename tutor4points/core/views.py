from django.contrib.auth import authenticate, login
from .forms import RegisterForm, ProfilePicUploadForm, UpdateTutorProfileForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login(request):
    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data.get(
                'username'), password=form.cleaned_data.get('password1'))
            messages.info(
                request, "Thanks for registering. You are now logged in.")
            login(request, new_user)
            return redirect("/register2")

    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


@login_required
# registration part 2 view
def register2(request):
    if request.method == "POST":
        form = ProfilePicUploadForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        if "no_tutor" in request.POST:
            return redirect("/dashboard")
        if "yes_tutor" in request.POST:
            return redirect("/update-tutor-profile")
    else:
        form = ProfilePicUploadForm()
    return render(request, "register2.html", {"form": form})


@login_required
# page allowing user to upate/creatae tutor profile
def update_tutor_profile(request):
    if request.method == "POST":
        form = UpdateTutorProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
        return redirect("/dashboard")

    else:
        form = UpdateTutorProfileForm()
    return render(request, "update_tutor_profile.html", {"form": form})


@login_required
# dashboard page
def dashboard(request):
    return render(request, "dashboard.html")
