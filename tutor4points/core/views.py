from .forms import RegisterForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, forms
from django.contrib.auth.decorators import login_required


def login_user(request):
    if request.method == "POST":
        form = forms.AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('/login')
    else:
        form = forms.AuthenticationForm()
    return render(request, "login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            new_user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1'))
            login(request, new_user)
            return redirect("/home")

    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


@login_required
# dahshboard/home page
def home(request):
    return render(request, "home.html")
