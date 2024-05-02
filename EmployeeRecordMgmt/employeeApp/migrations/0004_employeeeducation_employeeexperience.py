# Generated by Django 5.0.2 on 2024-03-05 16:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeApp', '0003_alter_employeedetail_gender'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeEducation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_pg', models.CharField(max_length=100, null=True)),
                ('college_pg', models.CharField(max_length=200, null=True)),
                ('passing_year_pg', models.CharField(max_length=20, null=True)),
                ('percentage_pg', models.CharField(max_length=30, null=True)),
                ('course_ug', models.CharField(max_length=100, null=True)),
                ('college_ug', models.CharField(max_length=200, null=True)),
                ('passing_year_ug', models.CharField(max_length=20, null=True)),
                ('percentage_ug', models.CharField(max_length=30, null=True)),
                ('course_ssc', models.CharField(max_length=100, null=True)),
                ('college_ssc', models.CharField(max_length=200, null=True)),
                ('passing_year_ssc', models.CharField(max_length=20, null=True)),
                ('percentage_ssc', models.CharField(max_length=30, null=True)),
                ('course_hsc', models.CharField(max_length=100, null=True)),
                ('college_hsc', models.CharField(max_length=200, null=True)),
                ('passing_year_hsc', models.CharField(max_length=20, null=True)),
                ('percentage_hsc', models.CharField(max_length=30, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cmp1_name', models.CharField(max_length=100, null=True)),
                ('cmp1_designation', models.CharField(max_length=100, null=True)),
                ('cmp1_salary', models.CharField(max_length=100, null=True)),
                ('cmp1_duration', models.CharField(max_length=100, null=True)),
                ('cmp2_name', models.CharField(max_length=100, null=True)),
                ('cmp2_designation', models.CharField(max_length=100, null=True)),
                ('cmp2_salary', models.CharField(max_length=100, null=True)),
                ('cmp2_duration', models.CharField(max_length=100, null=True)),
                ('cmp3_name', models.CharField(max_length=100, null=True)),
                ('cmp3_designation', models.CharField(max_length=100, null=True)),
                ('cmp3_salary', models.CharField(max_length=100, null=True)),
                ('cmp3_duration', models.CharField(max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]