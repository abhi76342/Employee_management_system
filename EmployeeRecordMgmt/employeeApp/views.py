from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from .forms import AddEducationForm, AddExperienceForm
from .forms import UserRegistrationForm
from .models import EmployeeDetail, EmployeeEducation, EmployeeExperience, EmploymentExperience


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('emp_home')

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"New account created: {user.username}")
            return redirect('/')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name="registration/register.html",
        context={"form": form}
    )


@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index")


def custom_login(request):
    if request.user.is_authenticated:
        return redirect("homepage")

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect("emp_home")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = AuthenticationForm()

    return render(
        request=request,
        template_name="registration/login.html",
        context={"form": form}
    )


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index")


def emp_home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'emp_home.html')


def profile(request):
    error = ""
    user = request.user
    try:
        employee = EmployeeDetail.objects.get(user=user)
    except ObjectDoesNotExist:
        employee = None

    gender_choices = EmployeeDetail.GENDER_CHOICES

    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        empid = request.POST.get('employeeId')
        email = request.POST.get('email')
        contact = request.POST.get('contact', '')
        department = request.POST.get('department', '')
        designation = request.POST.get('designation', '')
        joining_date = request.POST.get('joining_date', '')
        gender = request.POST.get('gender', '')

        try:
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.save()

            if employee:
                employee.employeeId = empid
                employee.contact = contact
                employee.empDept = department
                employee.designation = designation
                employee.joining_date = joining_date
                employee.gender = gender
                employee.save()
            else:
                employee = EmployeeDetail.objects.create(
                    user=user, employeeId=empid, contact=contact, empDept=department,
                    designation=designation, joining_date=joining_date, gender=gender
                )

            error = "no"
        except Exception as e:
            error = "yes"

    return render(request, 'profile.html',
                  {'error': error, 'user': user, 'employee': employee, 'gender_choices': gender_choices})


def admin_login(request):
    return render(request, 'admin_login.html')


def emp_experience(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    try:
        employee_experience = EmployeeExperience.objects.get(user=user)
        experiences = employee_experience.experience.all()  # Get all related experiences
    except EmployeeExperience.DoesNotExist:
        experiences = []

    return render(request, 'emp_experience.html', {'experiences': experiences})


def add_experience(request):
    error = ""
    user = request.user
    experiences = []
    try:
        employee_experience = EmployeeExperience.objects.get(user=user)
    except ObjectDoesNotExist:
        employee_experience = None

    if request.method == "POST":
        form = AddExperienceForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            designation = form.cleaned_data['designation']
            salary = form.cleaned_data['salary']
            duration = form.cleaned_data['duration']
            try:
                if employee_experience:
                    experience = EmploymentExperience.objects.create(user=user, company_name=company_name,
                                                                     designation=designation, salary=salary,
                                                                     duration=duration)
                    employee_experience.experience.add(experience)
                else:
                    employee_experience = EmployeeExperience.objects.create(user=user)
                    experience = EmploymentExperience.objects.create(user=user, company_name=company_name,
                                                                     designation=designation, salary=salary,
                                                                     duration=duration)
                    employee_experience.experience.add(experience)
                return redirect('emp_experience')
            except Exception as e:
                error = "yes"

        else:
            error = "no"

    else:
        form = AddExperienceForm()
        # Fetch all experiences if available
        try:
            if employee_experience:
                experiences = employee_experience.experience.all()
            else:
                experiences = []
        except ObjectDoesNotExist:
            pass

    return render(request, 'add_experience.html', {'form': form, 'experiences': experiences, 'error': error})


def delete_selected_experiences(request):
    if request.method == 'POST':
        selected_experience_ids = request.POST.getlist('selected_experiences')
        if not selected_experience_ids:
            messages.error(request, "No experiences selected for deletion.")
            return redirect('emp_experience')
        try:
            experiences_to_delete = EmploymentExperience.objects.filter(id__in=selected_experience_ids)
            experiences_to_delete.delete()
            messages.success(request, "Selected experiences deleted successfully.")
        except EmploymentExperience.DoesNotExist:
            messages.error(request, "Selected experiences do not exist.")
        return redirect('emp_experience')
    return redirect('emp_experience')


def delete_experience(request, experience_id):
    experience = get_object_or_404(EmploymentExperience, id=experience_id)
    experience.delete()
    messages.success(request, "Experience deleted successfully.")
    return redirect('emp_experience')


def emp_education(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    try:
        employee_education = EmployeeEducation.objects.get(user=user)
        educations = {
            'pg': employee_education.pg,
            'ug': employee_education.ug,
            'ssc': employee_education.ssc,
            'hsc': employee_education.hsc
        }
    except EmployeeEducation.DoesNotExist:
        educations = {}

    return render(request, 'emp_education.html', {'educations': educations})


def add_education(request):
    error = ""
    user = request.user
    educations = []

    try:
        employee_education = EmployeeEducation.objects.get(user=user)
    except ObjectDoesNotExist:
        employee_education = None

    if request.method == "POST":
        form = AddEducationForm(request.POST)
        if form.is_valid():
            pg = form.cleaned_data['pg']
            ug = form.cleaned_data['ug']
            ssc = form.cleaned_data['ssc']
            hsc = form.cleaned_data['hsc']
            try:
                if employee_education:
                    education = EmployeeEducation.objects.create(user=user, pg=pg, ug=ug, ssc=ssc, hsc=hsc)
                    employee_education.education.add(education)
                else:
                    employee_education = EmployeeEducation.objects.create(user=user)
                    education = EmployeeEducation.objects.create(user=user, pg=pg, ug=ug, ssc=ssc, hsc=hsc)
                    employee_education.education.add(education)
                return redirect('emp_education')
            except Exception as e:
                error = "An error occurred while saving education details."
        else:
            error = "Invalid form data"
    else:
        form = AddEducationForm()

    try:
        if employee_education:
            educations = employee_education.education.all()
    except ObjectDoesNotExist:
        pass

    return render(request, 'add_education.html', {'form': form, 'educations': educations, 'error': error})


def delete_education(request, education_type):
    user = request.user
    employee_education = get_object_or_404(EmployeeEducation, user=user)

    # Delete the selected education record
    if education_type in ['pg', 'ug', 'ssc', 'hsc']:
        setattr(employee_education, education_type, None)
        employee_education.save()
        messages.success(request, f"{education_type.upper()} education deleted successfully.")
    else:
        messages.error(request, "Invalid education type.")

    return redirect('emp_education')


@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'password_change.html', {'form': form})


def delete_selected_educations():
    return None


def terms_view(request):
    return render(request, 'terms.html')
