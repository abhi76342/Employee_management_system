# Generated by Django 5.0.2 on 2024-03-10 18:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeApp', '0010_rename_experiences_employeeexperience_experience'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeeducation',
            name='hsc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='hsc_education', to='employeeApp.education'),
        ),
        migrations.AlterField(
            model_name='employeeeducation',
            name='pg',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pg_education', to='employeeApp.education'),
        ),
        migrations.AlterField(
            model_name='employeeeducation',
            name='ssc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ssc_education', to='employeeApp.education'),
        ),
        migrations.AlterField(
            model_name='employeeeducation',
            name='ug',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ug_education', to='employeeApp.education'),
        ),
        migrations.AlterField(
            model_name='employeeeducation',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='education', to=settings.AUTH_USER_MODEL),
        ),
    ]
