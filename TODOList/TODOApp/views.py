from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime


# Create your views here.
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request, "Invalid username. Try again")
            return redirect('/login')
        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "No user found. Please register.")
            return redirect('/register')
        else:
            login(request, user)
            return redirect('/tasks')

    return render(request, 'login.html')


def register_page(request):
    if request.method == "POST":
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('rpassword')

        user = User.objects.filter(email=email)

        if user.exists():
            messages.info(request, "Account already exists")
            return redirect('/register')

        user = User.objects.create(
            first_name=firstname,
            last_name=lastname,
            email=email,
            username=email
        )
        print(user)
        user.set_password(password)
        user.save()
        return redirect('/login')

    return render(request, 'register.html')


def add_tasks(request):
    if request.method == "POST":
        task_name = request.POST.get('task_name')
        task_description = request.POST.get('task_description')
        status = request.POST.get('status')
        created_date = datetime.datetime.now()
        updated_date = datetime.datetime.now()
        if status:
            status = True
        else:
            status = False

        Tasks.objects.create(
            user=request.user,
            task_name=task_name,
            task_description=task_description,
            created_date=created_date,
            updated_date=updated_date,
            is_complete=status
        )
        queryset = Tasks.objects.all()
        context = {'tasks': queryset}
        return redirect('/tasks', context)
    return render(request, 'add_tasks.html')


# @login_required(login_url="/login")
def tasks_page(request):
    queryset = Tasks.objects.filter(user_id=request.user.id)
    context = {'tasks': queryset}
    return render(request, 'tasks.html', context)


def logout_page(request):
    logout(request)
    return redirect('/login')
