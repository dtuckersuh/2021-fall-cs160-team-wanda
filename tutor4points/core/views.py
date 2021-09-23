from .forms import AddClassForm, RegisterForm, AddTutorTimeForm
from django.shortcuts import render, redirect
from django.contrib import messages

# registration view


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/add-tutor-info")

    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})

# View to add tutor school, class, and time


def add_tutor_info(request):
    if request.method == "POST":
        if 'add_class' in request.POST:
            add_class_form = AddClassForm(request.POST)
            if add_class_form.is_valid():
                add_class_form.save()
        elif 'add_tutor_time' in request.POST:
            add_tutor_time_form = AddTutorTimeForm(request.POST)
            if add_tutor_time_form.is_valid():
                add_tutor_time_form.save()
        return redirect("/")

    else:
        add_class_form = AddClassForm()
        add_tutor_time_form = AddTutorTimeForm()
    return render(request, "add_tutor_info.html", {'add_class_form': add_class_form, 'add_tutor_time_form': add_tutor_time_form})
