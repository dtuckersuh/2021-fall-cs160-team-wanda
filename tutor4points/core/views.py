from django.contrib.auth import authenticate, login, forms
from .forms import RegisterForm, ProfilePicUploadForm, UpdateTutorProfileForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login_user(request):
    if request.method == "POST":
        form = forms.AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get(
                'username'), password=form.cleaned_data.get('password'))

            if user is not None:
                login(request, user)
                return redirect('/dashboard')
            else:
                return redirect('/')
    else:
        form = forms.AuthenticationForm()
    return render(request, "login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data.get(
                'username'), password=form.cleaned_data.get('password1'))
            login(request, new_user)
            return redirect("/register2")

    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


@ login_required
# registration part 2 view
def register2(request):
    if request.method == "POST":
        form = ProfilePicUploadForm(
            request.POST, request.FILES, instance=request.user)
        if "no_tutor" in request.POST:
            if form.is_valid():
                form.save()
            return redirect("/dashboard")
        if "yes_tutor" in request.POST:
            if form.is_valid():
                profile = form.save(commit=False)
                profile.is_tutor = True  # mark that person wants to be a tutor
                profile.save()
            return redirect("/update-tutor-profile")
    else:
        form = ProfilePicUploadForm()
    return render(request, "register2.html", {"form": form})


@ login_required
# page allowing user to upate/create tutor profile
def update_tutor_profile(request):
    if request.method == "POST":
        form = UpdateTutorProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect("/dashboard")

    else:
        form = UpdateTutorProfileForm()
    return render(request, "update_tutor_profile.html", {"form": form})


@ login_required
# dashboard page
def dashboard(request):
    return render(request, "dashboard.html")
