from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from django.shortcuts import render, redirect

from . import forms

from .models import Employee


# Import other necessary modules if needed

# Rest of your views...

# Create your views here.
def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')


def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render(request, 'view_all_emp.html', context)


def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])
        new_emp = Employee(first_name=first_name, last_name=last_name, salary=salary, phone=phone, bonus=bonus,
                           dept_id=dept, role_id=role, hire_date=timezone.now())
        new_emp.save()
        return HttpResponse("Employee Added Successfully")
    elif request.method == 'GET':
        print('get')
        return render(request, 'add_emp.html')
    else:
        return HttpResponse("An Exception Occurred! Employee has not been added ")


def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee removed Successfully")
        except Employee.DoesNotExist:
            return HttpResponse("Please Enter a valid ID")
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'remove_emp.html', context)


def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']

        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role_name__icontains=role)
        context = {
            'emps': emps
        }
        return render(request, 'view_all_emp.html', context)
    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse("An Error occurred!")


def user_register(request):
    if request.method == "GET":
        register_form = forms.RegisterForm()
        return render(request, "signup.html", {'form': register_form})
    else:
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            first_name = register_form.cleaned_data['first_name']
            last_name = register_form.cleaned_data['last_name']
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            confirm_password = register_form.cleaned_data['confirm_password']

            if password == confirm_password:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already in use.')
                    return redirect('register')
                elif User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already taken.')
                    return redirect('register')
                else:
                    # Create the user
                    user = User.objects.create_user(username=username,
                                                    email=email,
                                                    password=password,
                                                    first_name=first_name,
                                                    last_name=last_name)
                    messages.success(request, 'Registration successful. Please log in.')
                    return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')
                return redirect('register')
        else:
            # Render the registration form with validation errors
            return render(request, "signup.html", {'form': register_form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')
