from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import EmploymentExperience, Education


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


class AddEducationForm(forms.Form):
    EDUCATION_LEVELS = ['pg', 'ug', 'ssc', 'hsc']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for level in self.EDUCATION_LEVELS:
            self.fields[level + '_course'] = forms.CharField(max_length=100, required=False)
            self.fields[level + '_college'] = forms.CharField(max_length=200, required=False)
            self.fields[level + '_passing_year'] = forms.CharField(max_length=20, required=False)
            self.fields[level + '_percentage'] = forms.CharField(max_length=30, required=False)

    def clean(self):
        cleaned_data = super().clean()
        for level in self.EDUCATION_LEVELS:
            course = cleaned_data.get(level + '_course')
            college = cleaned_data.get(level + '_college')
            passing_year = cleaned_data.get(level + '_passing_year')
            percentage = cleaned_data.get(level + '_percentage')

            if course and not (college and passing_year and percentage):
                self.add_error(level + '_course', "All fields are required if course is provided.")
                self.add_error(level + '_college', "")
                self.add_error(level + '_passing_year', "")
                self.add_error(level + '_percentage', "")

        return cleaned_data

    def save(self, user):
        education_data = {}
        for level in self.EDUCATION_LEVELS:
            education_data[level] = self.save_education(user, level)
        return education_data

    def save_education(self, user, level):
        course = self.cleaned_data.get(level + '_course')
        college = self.cleaned_data.get(level + '_college')
        passing_year = self.cleaned_data.get(level + '_passing_year')
        percentage = self.cleaned_data.get(level + '_percentage')

        if course and college and passing_year and percentage:
            return Education.objects.create(
                course=course,
                college=college,
                passing_year=passing_year,
                percentage=percentage,
                user=user
            )
        return None


class AddExperienceForm(forms.ModelForm):
    class Meta:
        model = EmploymentExperience
        fields = ['company_name', 'designation', 'salary', 'duration']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Designation'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salary'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Duration'}),
        }
