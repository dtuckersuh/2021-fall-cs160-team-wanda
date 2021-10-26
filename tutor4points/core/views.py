from .forms import RegisterForm, UpdateProfileForm, PurchasePointsForm, CashOutPointsForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, forms
from django.contrib.auth.decorators import login_required


# loginUser handles "/login" endpoint
# logs in the user that has the specified login credentials from the login form
def loginUser(request):
    if request.user.is_authenticated:
        return redirect ("home")
    elif request.method == "POST":
        form = forms.AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('login')
    else:
        form = forms.AuthenticationForm()
    return render(request, "login.html", {"form": form})


# register handles "/users/register" endpoint
# allows user to enter account information into register form, creates an account for the user, and logs them in
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            new_user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1'))
            login(request, new_user)
            return redirect("home")

    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


# home handles "/home" endpoint
# redirects to home page
@login_required
def home(request):
    if request.user.is_authenticated:
        return render(request, "home.html")
    else:
        return redirect ("")


# tutors handles "/tutors" endpoint
# allows user to view all tutors that attend the same school as them
@login_required
def tutors(request):
    if request.method == 'GET':
        current_user = request.user
        users = get_user_model().objects.all()
        tutors = users.filter(is_tutor=True, school=current_user.school)

        return render(request, 'tutors.html', {'tutors': tutors})


# users handles "/users/<int:id>" endpoint
# allows users to view profile of user specified by user id
# allows users to edit their profile
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

    return render(request, 'users_profile.html', {
        'user': user,
        'form': form,
        'current_user': request.user.id == id
    })


# home handles "/points" endpoint
# allows users to view current points, purchase points, or transfer points to tutors
@login_required
def points(request):
    # TODO add custom forms for points and replace forms below
    current_user = request.user
    users = get_user_model().objects.all()
    tutors = users.filter(is_tutor=True, school=current_user.school)
    if request.method == 'POST':
        form_purchase = PurchasePointsForm(request.POST, instance=request.user)
        if form_purchase.is_valid():
            form_purchase.save()
        form_cash_out = CashOutPointsForm(request.POST, instance=request.user)
        if form_cash_out.is_valid():
            form_cash_out.save()
    else:
        form_purchase = PurchasePointsForm()
        form_cash_out = CashOutPointsForm()
    return render(
        request, "points.html", {
            'user': request.user,
            'form_purchase': form_purchase,
            'form_cash_out': form_cash_out,
            'tutors': tutors
        })
