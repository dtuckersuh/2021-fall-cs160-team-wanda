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
    error = '' #blank error
    if request.method == 'POST': #if we get a post
        form_purchase = PurchasePointsForm(request.POST) #create the forms
        form_cash_out = CashOutPointsForm(request.POST)
        form_transfer = TransferPointsForm(request.POST, user = request.user)
        if 'purchase' in request.POST: #if we got a purchase
            if form_purchase.is_valid(): #validate
                if(form_purchase.cleaned_data['purchased_points'] != None): #make sure they entered a number
                    if (form_purchase.cleaned_data['purchased_points'] > 0): #validate data
                        current_user.total_points +=form_purchase.cleaned_data['purchased_points'] #save if positive
                        current_user.save()
                    else:
                        error = "Enter a positive value for points purchased" #or else send an error
                else:
                    error = "Please enter a value for points purchased" #or else send an error
        elif 'cash_out' in request.POST:  #Same with cash out
            if form_cash_out.is_valid():
                if(form_cash_out.cleaned_data['cashed_points'] != None):
                    if (form_cash_out.cleaned_data['cashed_points'] > 0 and form_cash_out.cleaned_data['cashed_points'] <= request.user.total_points ):
                        current_user.total_points -=form_cash_out.cleaned_data['cashed_points']
                        current_user.save()
                    elif(form_cash_out.cleaned_data['cashed_points'] > 0):
                        error = "Enter a value less than or equal to your current points for points redeemed" #two different errors depending on data
                    else:
                        error = "Enter a positive value for points redeemed"
                else:
                    error = "Please enter a value for points redeemed"
        elif 'transfer' in request.POST: #same with transfer
                if form_transfer.is_valid():
                    if(form_transfer.cleaned_data['amount_to_transfer'] != None and form_transfer.cleaned_data['tutors'] != None):
                        if(form_transfer.cleaned_data['amount_to_transfer'] > 0 and form_transfer.cleaned_data['amount_to_transfer'] <= request.user.total_points):
                            current_user.total_points -= form_transfer.cleaned_data['amount_to_transfer']
                            current_user.save()
                            form_transfer.cleaned_data['tutors'].total_points += form_transfer.cleaned_data['amount_to_transfer'] #make sure
                            form_transfer.cleaned_data['tutors'].save()
                        elif(form_transfer.cleaned_data['amount_to_transfer'] > 0):
                            error = "Enter a value less than or equal to your current points for points transferred"
                        else:
                            error = "Enter a positive value for points transferred"
                    else:
                        error = "Please enter a value for tutor and points transferred"

    else:
        form_purchase = PurchasePointsForm()
        form_cash_out = CashOutPointsForm()
        form_transfer = TransferPointsForm(user = request.user)
    return render(
        request, "points.html", {
            'user': request.user,
            'form_purchase': form_purchase,
            'form_cash_out': form_cash_out,
            'tutors': tutors,
            'form_transfer_points': form_transfer,
            'error_message' : error
        })
