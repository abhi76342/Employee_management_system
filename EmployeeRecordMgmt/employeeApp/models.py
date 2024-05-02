from django.contrib.auth.models import User
from django.db import models


class EmployeeDetail(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Prefer not to say', 'Prefer not to say'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employeeId = models.CharField(max_length=50)
    empDept = models.CharField(max_length=100)
    designation = models.CharField(max_length=50, null=True)
    contact = models.CharField(max_length=15, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True)
    joining_date = models.DateField(null=True)

    def __str__(self):
        return self.user.username


class Education(models.Model):
    course = models.CharField(max_length=100)
    college = models.CharField(max_length=200)
    passing_year = models.CharField(max_length=20)
    percentage = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.course} - {self.college}"


class EmployeeEducation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='education')
    education = models.ManyToManyField(Education)
    pg = models.ForeignKey(Education, related_name='pg_education', on_delete=models.SET_NULL, null=True)
    ug = models.ForeignKey(Education, related_name='ug_education', on_delete=models.SET_NULL, null=True)
    ssc = models.ForeignKey(Education, related_name='ssc_education', on_delete=models.SET_NULL, null=True)
    hsc = models.ForeignKey(Education, related_name='hsc_education', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username


class EmploymentExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, null=True)
    designation = models.CharField(max_length=100, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    duration = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.company_name}"


class EmployeeExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experience = models.ManyToManyField(EmploymentExperience)

    def __str__(self):
        return self.user.username
