from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Employee, Department
from .forms import (
    SignupForm,
    LoginForm,
    EmployeeForm,
    DepartmentForm,
    EmployeeSearchForm,
)


def signup_view(request):
   
    if request.user.is_authenticated:
        return redirect('dashboard')

    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect(next_url or 'dashboard')
    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {'form': form, 'next': next_url})


def login_view(request):
   
    if request.user.is_authenticated:
        return redirect('dashboard')

    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(next_url or 'dashboard')
    else:
        form = LoginForm(request)

    return render(request, 'registration/login.html', {'form': form, 'next': next_url})


def logout_view(request):
   
    logout(request)
    return redirect('login')


def dashboard(request):
    
    search_form = EmployeeSearchForm(request.GET or None)

   
    employees_qs = Employee.objects.select_related('department').all()

    if search_form.is_valid():
        q = search_form.cleaned_data.get('q')
        department = search_form.cleaned_data.get('department')

        if q:
            employees_qs = employees_qs.filter(Q(name__icontains=q) | Q(email__icontains=q))

        if department:
            employees_qs = employees_qs.filter(department=department)

    context = {
        'employees': employees_qs,
        'search_form': search_form,
        'total_employees': Employee.objects.count(),
        'total_departments': Department.objects.count(),
    }

    return render(request, 'employees/dashboard.html', context)


@login_required
def employee_create(request):
  
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            emp = form.save()
            messages.success(request, f'"{emp.name}" added successfully.')
            return redirect('dashboard')
    else:
        form = EmployeeForm()

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Add Employee',
        'submit_label': 'Add Employee',
    })


@login_required
def employee_edit(request, pk):
    
    emp = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{emp.name}" updated.')
            return redirect('dashboard')
    else:
        form = EmployeeForm(instance=emp)

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': f'Edit {emp.name}',
        'submit_label': 'Save Changes',
    })


@login_required
def employee_delete(request, pk):
    emp = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        name = emp.name
        emp.delete()
        messages.success(request, f'"{name}" deleted.')
        return redirect('dashboard')

    return render(request, 'employees/employee_confirm_delete.html', {'employee': emp})


@login_required
def department_list(request):
   
    departments = Department.objects.all()
    return render(request, 'employees/department_list.html', {'departments': departments})


@login_required
def department_create(request):
   
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save()
            messages.success(request, f'"{dept.name}" created.')
            return redirect('department_list')
    else:
        form = DepartmentForm()

    return render(request, 'employees/department_form.html', {
        'form': form,
        'title': 'Add Department',
        'submit_label': 'Create',
    })


@login_required
def department_edit(request, pk):
   
    dept = get_object_or_404(Department, pk=pk)

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{dept.name}" updated.')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=dept)

    return render(request, 'employees/department_form.html', {
        'form': form,
        'title': f'Edit {dept.name}',
        'submit_label': 'Save',
    })