# Generated by Django 5.0.2 on 2024-03-05 00:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employeeApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeedetail',
            old_name='empId',
            new_name='employeeId',
        ),
    ]
