from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Authentication URLs
    path("register", views.register, name="register"),
    path('login', views.custom_login, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('password_change/', views.password_change, name="password_change"),

    # Profile and Home URLs
    path('', views.index, name="index"),  # Root URL pattern
    path('profile/', views.profile, name="profile"),
    path('emp_home/', views.emp_home, name="emp_home"),
    path('terms/', views.terms_view, name='terms'),

    # Admin URLs
    path('admin_login/', views.admin_login, name="admin_login"),

    # Experience URLs
    path('emp_experience/', views.emp_experience, name="emp_experience"),
    path('add_experience/', views.add_experience, name="add_experience"),
    path('delete/<int:experience_id>/', views.delete_experience, name='delete_experience'),
    path('delete_selected/', views.delete_selected_experiences, name='delete_selected_experiences'),

    # Education URLs
    path('emp_education/', views.emp_education, name="emp_education"),
    path('add_education/', views.add_education, name="add_education"),
    path('delete_education/<int:education_id>/', views.delete_education, name='delete_education'),
    path('delete_selected_educations/', views.delete_selected_educations, name='delete_selected_educations'),
]
