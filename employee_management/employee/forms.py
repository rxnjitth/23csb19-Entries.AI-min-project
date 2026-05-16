from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Employee, Department
import re
from datetime import date


class SignupForm(UserCreationForm):
	
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if email and User.objects.filter(email__iexact=email).exists():
			raise forms.ValidationError('Email already registered.')
		return email


class LoginForm(AuthenticationForm):
	
	pass


class EmployeeForm(forms.ModelForm):
	

	class Meta:
		model = Employee
		fields = ['name', 'email', 'department', 'salary', 'joining_date']

	def clean_name(self):
		name = (self.cleaned_data.get('name') or '').strip()
		if len(name) < 2:
			raise forms.ValidationError('Name must be at least 2 characters.')
		if not re.match(r"^[a-zA-Z\s\-'.]+$", name):
			raise forms.ValidationError('Name can only contain letters and spaces.')
		return name

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if not email:
			return email
		qs = Employee.objects.filter(email__iexact=email)
		if self.instance.pk:
			qs = qs.exclude(pk=self.instance.pk)
		if qs.exists():
			raise forms.ValidationError('This email is already used.')
		return email

	def clean_salary(self):
		salary = self.cleaned_data.get('salary')
		if salary is not None and salary < 0:
			raise forms.ValidationError('Salary cannot be negative.')
		return salary

	def clean_joining_date(self):
		joining_date = self.cleaned_data.get('joining_date')
		if joining_date and joining_date > date.today():
			raise forms.ValidationError('Joining date cannot be in the future.')
		return joining_date


class DepartmentForm(forms.ModelForm):
	class Meta:
		model = Department
		fields = ['name']

	def clean_name(self):
		name = (self.cleaned_data.get('name') or '').strip()
		qs = Department.objects.filter(name__iexact=name)
		if self.instance.pk:
			qs = qs.exclude(pk=self.instance.pk)
		if qs.exists():
			raise forms.ValidationError('Department already exists.')
		return name


class EmployeeSearchForm(forms.Form):
	q = forms.CharField(required=False)
	department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, empty_label='All')
