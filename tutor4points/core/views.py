from .forms import RegisterForm, TutorRequestForm, UpdateProfileForm, PurchasePointsForm, CashOutPointsForm, TransferPointsForm, RequestResponseForm, RateTutorForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import TutorRequest, Rating


# loginUser handles "/login" endpoint
# logs in the user that has the specified login credentials from the login form
def loginUser(request):
    if request.user.is_authenticated:
        return redirect("home")
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
    success_message = ""
    tutor_instance = None
    if current_user.is_authenticated:
        users = get_user_model().objects.all().exclude(pk=current_user.id)
        tutors = users.filter(is_tutor=True, school=current_user.school)
        requests_received = TutorRequest.objects.all().filter(
            tutor=current_user, accepted=None, completed=False)
        sent_requests = TutorRequest.objects.all().filter(tutee=current_user,
                                                          completed=False)
        if request.method == 'POST' and 'submit-accept-request' in request.POST:
            form_request_response = RequestResponseForm(
                request.POST,
                accepted=True,
                request_id=request.POST['request-id'])
            if form_request_response.is_valid():
                form_request_response.save()
                form_request_response = RequestResponseForm(
                )  #reset form after submission
        else:
            form_request_response = RequestResponseForm()

        if request.method == 'POST' and 'submit-decline-request' in request.POST:
            print("DECLINE")
            form_request_response = RequestResponseForm(
                request.POST,
                accepted=False,
                request_id=request.POST['request-id'])
            if form_request_response.is_valid():
                form_request_response.save()
                form_request_response = RequestResponseForm(
                )  #reset form after submission
        else:
            form_request_response = RequestResponseForm()

        if request.method == 'POST' and 'submit-tutor-request' in request.POST:
            form_request_tutor = TutorRequestForm(request.POST)
            if form_request_tutor.is_valid():
                tutor_instance = get_user_model().objects.get(
                    pk=request.POST['requestedTutor'])  # get tutor object
                tutor_request = form_request_tutor.save(commit=False)
                tutor_request.tutee = current_user
                tutor_request.tutor = tutor_instance
                tutor_request.save()
                success_message = "Success! You have sent a request to "
                form_request_tutor = TutorRequestForm(
                )  #reset form after submission
        else:
            form_request_tutor = TutorRequestForm()

        return render(
            request, "home.html", {
                'tutors': tutors,
                'requests_received': requests_received,
                'sent_requests': sent_requests,
                'form_request_tutor': form_request_tutor,
                'form_request_response': form_request_response,
                'success_message': success_message,
                'tutor_instance': tutor_instance
            })
    else:
        return redirect("")


# tutors handles "/tutors" endpoint
# allows user to view all tutors that attend the same school as them and send a tutor request
@login_required
def tutors(request):
    current_user = request.user
    users = get_user_model().objects.all().exclude(pk=current_user.id)
    tutors = users.filter(is_tutor=True, school=current_user.school)
    success_message = ""
    tutor_instance = None
    if request.method == 'POST':
        form = TutorRequestForm(request.POST)
        if (form.is_valid()):
            tutor_instance = get_user_model().objects.get(
                pk=request.POST['requestedTutor'])  # get tutor object
            tutor_request = form.save(commit=False)
            tutor_request.tutee = current_user
            tutor_request.tutor = tutor_instance
            tutor_request.save()
            success_message = "Success! You have sent a request to "
            form = TutorRequestForm()
    else:
        form = TutorRequestForm()

    return render(
        request, 'tutors.html', {
            'users': users,
            'user': current_user,
            'tutors': tutors,
            'form': form,
            'success_message': success_message,
            'tutor_instance': tutor_instance
        })


# users handles "/users/<int:id>" endpoint
# allows users to view profile of user specified by user id and edit their own profile
@login_required
def users(request, id):

    # get user that is specified by URL
    user = get_user_model().objects.get(pk=id)
    success_message = ""
    if request.method == 'POST' and 'email' in request.POST:
        form_update_profile = UpdateProfileForm(request.POST,
                                                request.FILES,
                                                instance=user)

        if form_update_profile.is_valid():
            form_update_profile.save()
    else:
        form_update_profile = UpdateProfileForm(instance=user)

    if request.method == 'POST' and 'request-tutor' in request.POST:
        form_tutor_request = TutorRequestForm(request.POST)
        if form_tutor_request.is_valid():
            tutor_request = form_tutor_request.save(commit=False)
            tutor_request.tutee = request.user
            tutor_request.tutor = user
            tutor_request.save()
            success_message = "Success! You have sent a request to "
            form_tutor_request = TutorRequestForm()
    else:
        form_tutor_request = TutorRequestForm()

    return render(
        request, 'users_profile.html', {
            'user': user,
            'form_update_profile': form_update_profile,
            'form_tutor_request': form_tutor_request,
            'current_user': request.user.id == id,
            'success_message': success_message
        })


# home handles "/points" endpoint
# allows users to view current points, purchase points, or transfer points to tutors
@login_required
def points(request):
    current_user = request.user  #the user
    users = get_user_model().objects.all()  #list of users to display
    tutors = users.filter(is_tutor=True, school=current_user.school)
    success_message = ""

    if request.method == 'POST' and 'purchase' in request.POST:  #if we get a post and got a purchase
        form_purchase = PurchasePointsForm(
            request.POST, user=request.user)  #create the forms
        if form_purchase.is_valid():  #validate data
            form_purchase.save()
            points_purchase = form_purchase.cleaned_data['purchased_points']
            success_message = f"Success! You have purchased {points_purchase} points for {'${:,.2f}'.format(points_purchase * 0.01)}."
            form_purchase = PurchasePointsForm(
                user=request.user
            )  #show empty form (reset fields) after form successfully submitted
    else:
        form_purchase = PurchasePointsForm(user=request.user)

    if request.method == 'POST' and 'cash-out' in request.POST:  #if we get a post and cash out
        form_cash_out = CashOutPointsForm(request.POST, user=request.user)

        if form_cash_out.is_valid():  #validate data
            form_cash_out.save()  #save if positive
            points_cash_out = form_cash_out.cleaned_data['cashed_points']
            success_message = f"Success! You have cashed out {points_cash_out} points for {'${:,.2f}'.format(points_cash_out * 0.009)}."
            form_cash_out = CashOutPointsForm(
                user=request.user
            )  #show empty form (reset fields) after form successfully submitted
    else:
        form_cash_out = CashOutPointsForm(user=request.user)

    if request.method == 'POST' and 'transfer' in request.POST:  #if we get a post and cash out
        form_transfer_points = TransferPointsForm(request.POST,
                                                  user=request.user)
        if form_transfer_points.is_valid():  #validate data
            form_transfer_points.save()
            success_message = f"Success! You have paid {form_transfer_points.cleaned_data['tutors']} {form_transfer_points.cleaned_data['amount_to_transfer']} points."
            form_transfer_points = TransferPointsForm(
                user=request.user
            )  #show empty form (reset fields) after form successfully submitted
    else:
        form_transfer_points = TransferPointsForm(user=request.user)

    return render(
        request, "points.html", {
            'user': request.user,
            'form_purchase': form_purchase,
            'form_cash_out': form_cash_out,
            'tutors': tutors,
            'form_transfer_points': form_transfer_points,
            'success_message': success_message,
        })


# requests handles "users/<int:id>/requests" endpoint
# allows users to view requests sent and received as well as accept/decline received requests
@login_required
def requests(request, id):
    current_user = request.user
    requests_received = TutorRequest.objects.all().filter(
        tutor=current_user, completed=False)  # get all user's tutor requests
    requests_sent = TutorRequest.objects.all().filter(
        tutee=current_user,
        tutee_completed=False)  # get all user's tutor requests
    accept_filter = ""
    if request.method == 'POST' and 'submit-accept-request' in request.POST:
        form_request_response = RequestResponseForm(
            request.POST, accepted=True, request_id=request.POST['request-id'])
        if form_request_response.is_valid():
            form_request_response.save()
            form_request_response = RequestResponseForm()
    elif request.method == 'POST' and 'submit-decline-request' in request.POST:
        form_request_response = RequestResponseForm(
            request.POST,
            accepted=False,
            request_id=request.POST['request-id'])
        if form_request_response.is_valid():
            form_request_response.save()
            form_request_response = RequestResponseForm()
    else:
        form_request_response = RequestResponseForm()
    if request.method == "POST" and 'show-accepted' in request.POST:
        requests_received = requests_received.filter(accepted=True)
        requests_sent = requests_sent.filter(accepted=True)
        accept_filter = "checked"

    if request.method == 'POST' and 'submit-rating' in request.POST:  #code for rating, move once 'paid and done' functionality is added.
        form_rating = RateTutorForm(request.POST)
        if form_rating.is_valid():
            rating = form_rating.save(commit=False)  #create a rating form
            userGivenTo = get_user_model().objects.get(
                pk=request.POST['request-tutor']
            )  #get the user that its given to

            current_request = TutorRequest.objects.get(
                pk=request.POST['request-id'])  #get current requests data
            current_request.paid = True  # make sure the paid is true

            if 'complete' in request.POST and 'paid' in request.POST:  #continue only if paid and completed.
                rating.given_to = userGivenTo  #update the rating form
                rating.given_by = request.user
                # calcute new rating, and update the database
                if current_user != current_request.tutor:  #if the current user is the tutee, then give a tutor rating
                    rating.rating_type = 'tutor'  #set the tutor type
                    rating.save()  #save the rating

                    tutor_ratings = Rating.objects.filter(
                        given_to=userGivenTo).filter(
                            rating_type='tutor'
                        )  #grab all tutor ratings for the user
                    count = 0  #sum up the rating
                    sum = 0
                    for i in tutor_ratings:
                        count += 1
                        sum += i.rating
                    userGivenTo.tutor_avg_rating = sum / count  #geaverage

                    current_request.tutee_completed = True
                else:  #otherwise if the current user is a tutor, give a tutee
                    rating.rating_type = 'tutee'
                    rating.save()

                    tutor_ratings = Rating.objects.filter(
                        given_to=userGivenTo).filter(rating_type='tutee')
                    count = 0
                    sum = 0
                    for i in tutor_ratings:
                        count += 1
                        sum += i.rating
                    userGivenTo.tutee_avg_rating = sum / count

                    current_request.completed = True
                userGivenTo.save(
                )  #after branches come together, save the rating average
                current_request.save()  #save the requests completed and paid

    else:  # if not, then make sure we have a RateTutorForm
        form_rating = RateTutorForm()

    return render(
        request, 'requests.html', {
            'form_request_response': form_request_response,
            'requests_received': requests_received,
            'requests_sent': requests_sent,
            'accept_filter': accept_filter,
            'form_rating': form_rating
        })
