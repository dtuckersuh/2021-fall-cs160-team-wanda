from .forms import RegisterForm, UpdateProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, forms
from django.contrib.auth.decorators import login_required


def loginUser(request):
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


@login_required
def tutors(request):
    if request.method == 'GET':
        current_user = request.user
        users = get_user_model().objects.all()
        tutors = users.filter(is_tutor=True, school=current_user.school)

        return render(request, 'tutors.html', {'tutors': tutors})


@login_required
def users(request, id):

    # get user that is specified by URL
    user = get_user_model().objects.get(pk=id)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = UpdateProfileForm(instance=user)

    return render(request, 'users_profile.html', {'user': user, 'form': form, 'current_user': request.user.id == id})
