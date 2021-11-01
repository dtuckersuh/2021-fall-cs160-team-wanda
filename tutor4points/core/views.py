from .forms import RegisterForm, UpdateProfileForm, PurchasePointsForm, CashOutPointsForm,TransferPointsForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

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
    current_user = request.user
    if current_user.is_authenticated:
        users = get_user_model().objects.all().exclude(pk=current_user.id)
        tutors = users.filter(is_tutor=True, school=current_user.school)
        return render(request, "home.html", {"tutors": tutors})
    else:
        return redirect ("")


# tutors handles "/tutors" endpoint
# allows user to view all tutors that attend the same school as them
@login_required
def tutors(request):
    if request.method == 'GET':
        current_user = request.user
        users = get_user_model().objects.all().exclude(pk=current_user.id)
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
        form = UpdateProfileForm(request.POST, request.FILES, instance=user)
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
    current_user = request.user #the user
    users = get_user_model().objects.all() #list of users to display
    tutors = users.filter(is_tutor=True, school=current_user.school)
    success_message = ""

    if request.method == 'POST' and 'purchase' in request.POST: #if we get a post and got a purchase
        form_purchase = PurchasePointsForm(request.POST, user = request.user) #create the forms
        if form_purchase.is_valid(): #validate data
            form_purchase.save()
            points_purchase = form_purchase.cleaned_data['purchased_points']
            success_message = f"Success! You have purchased {points_purchase} points for {'${:,.2f}'.format(points_purchase * 0.01)}."
    else:
        form_purchase = PurchasePointsForm(user = request.user)

    if request.method == 'POST' and 'cash_out' in request.POST:  #if we get a post and cash out
        form_cash_out = CashOutPointsForm(request.POST, user = request.user)

        if form_cash_out.is_valid(): #validate data
            form_cash_out.save() #save if positive
            points_cash_out = form_cash_out.cleaned_data['cashed_points']
            success_message = f"Success! You have cashed out {points_cash_out} points for {'${:,.2f}'.format(points_cash_out * 0.009)}."
    else:
        form_cash_out = CashOutPointsForm(user = request.user)

    if request.method == 'POST' and 'transfer' in request.POST: #if we get a post and cash out
        form_transfer_points = TransferPointsForm(request.POST, user = request.user)
        if form_transfer_points.is_valid(): #validate data
            form_transfer_points.save()
            success_message = f"Success! You have paid {form_transfer_points.cleaned_data['tutors']} {form_transfer_points.cleaned_data['amount_to_transfer']} points."
    else:
        form_transfer_points = TransferPointsForm(user=request.user)

    return render(
        request, "points.html", {
            'user': request.user,
            'form_purchase': form_purchase,
            'form_cash_out': form_cash_out,
            'tutors': tutors,
            'form_transfer_points': form_transfer_points,
            'success_message': success_message,}
        )
