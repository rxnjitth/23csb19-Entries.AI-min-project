from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('auth/signup/', views.signup_view, name='signup'),
    path('auth/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('auth/logout/', views.logout_view, name='logout'),

    path('employees/add/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),

    path('departments/', views.department_list, name='department_list'),
    
]