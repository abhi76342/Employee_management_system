from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('home/', views.home, name='home'),
    path('signup/', auth_views.SignUpView.as_view(), name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('all_emp/', views.all_emp, name="all_emp"),
    path('add_emp', views.add_emp, name="add_emp"),
    path('remove_emp/', views.remove_emp, name="remove_emp"),
    path('remove_emp/<int:emp_id>/', views.remove_emp, name="remove_emp"),
    path('filter_emp', views.filter_emp, name="filter_emp"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Using built-in login view
]
