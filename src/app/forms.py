from django import forms
from django.contrib.auth import login, password_validation
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField, PasswordChangeForm, SetPasswordForm, 
    UserCreationForm, AuthenticationForm, PasswordResetForm
)
from ckeditor.widgets import CKEditorWidget

from .models import User, Applicant, Employer, Experience, Vacancy
from .choices import *


# help_text=password_validation.password_validators_help_text_html())

# APPLICANT

class ApplicantCreationForm(forms.ModelForm):
    first_name = forms.CharField(
        label='', widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        label='', widget=forms.TextInput(attrs={'placeholder': 'Last name'})
    )
    email = forms.EmailField(
        label='', widget=forms.TextInput(attrs={'placeholder': 'Email address'})
    )
    password1 = forms.CharField(
        label='', min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='', min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Password again'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_password(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        password_validation.validate_password(password2)
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class ApplicantEditForm(forms.ModelForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ApplicantProfileForm(forms.ModelForm):
    birthday = forms.DateField(label='', widget=forms.SelectDateWidget(years=YEARS)) 
    photo = forms.ImageField(required=False, widget=forms.FileInput, label='Your photo')
    location = forms.CharField(widget=forms.Select(choices=LOCATION), required=False)
    citizenship = forms.CharField(widget=forms.Select(choices=COUNTRIES), required=False)

    class Meta:
        model = Applicant
        fields = ('birthday', 'photo', 'location', 'citizenship')


class PhotoForm(forms.ModelForm):
    photo = forms.ImageField(required=False, widget=forms.FileInput, label='')

    class Meta:
        model = Applicant
        fields = ['photo']


class EducationForm(forms.ModelForm):
    education = forms.CharField(widget=forms.Select(choices=EDUCATION), label='Degree', required=False)
    specialization = forms.CharField(widget=forms.Select(choices=SPECIALIZATION), required=False)

    class Meta:
        model = Applicant
        fields = ['education', 'specialization']


class ExperienceForm(forms.ModelForm):
    # required_css_class = 'required'
    begin = forms.DateField(widget=forms.SelectDateWidget(years=WORK_YEARS), label='Beginning of work') 
    now = forms.BooleanField(label='To date', required=False)
    end = forms.DateField(widget=forms.SelectDateWidget(years=WORK_YEARS), label='Ending', required=False)
    company = forms.CharField(label='Company')
    company_site = forms.URLField(label='Site', required=False)
    company_spheres = forms.MultipleChoiceField(
        choices=SPHERES, widget=forms.CheckboxSelectMultiple(), label='Scopes of the company'
    )
    position = forms.ChoiceField(choices=SPECIALIZATION)
    responsibilities = forms.CharField(widget=CKEditorWidget(), label='Workplace responsibilities')

    class Meta:
        model = Experience
        fields = (
            'begin','now', 'end', 'company', 'company_site', 
            'company_spheres', 'position', 'responsibilities',
        )


class SkillsForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['skills']


class LanguagesForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['languages']


# EMPLOYEER 

class EmployerCreationForm(forms.ModelForm):
    first_name = forms.CharField(
        label='', widget=forms.TextInput(attrs={'autofocus': True,'placeholder': 'First name'})
    )
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    company = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Company'}))
    password1 = forms.CharField(
        label='', strip=False, min_length=8, widget=forms.PasswordInput(
            attrs={'placeholder': 'Password'}
        )
    )
    password2 = forms.CharField(
        label='', strip=False, min_length=8, widget=forms.PasswordInput(
            attrs={'placeholder': 'Password again'}
        )
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'company')

    def clean_password(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        password_validation.validate_password(password2)
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EmployerEditForm(forms.ModelForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Personal email'}))
    company = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Company'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'company')


class EmployerProfileForm(forms.ModelForm):
    company_email = forms.EmailField(
        required=False, label='', widget=forms.TextInput(attrs={'placeholder': 'Company email'})
    )
    company_site = forms.URLField(
        required=False, label='', widget=forms.TextInput(attrs={'placeholder': 'Company website'})
    )
    company_info = forms.CharField(
        required=False, label='About the company:', widget=CKEditorWidget()
    )
    company_spheres = forms.MultipleChoiceField(
        required=False, choices=SPHERES, widget=forms.CheckboxSelectMultiple(), label='Company scopes:'
    )

    class Meta:
        model = Employer
        fields = ('company_email', 'company_site', 'company_info', 'company_spheres')


class VacancyForm(forms.ModelForm):
    salary = forms.IntegerField(required=False, min_value=0)
    body = forms.CharField(widget=CKEditorWidget(), label='Description')
    need_exp = forms.ChoiceField(choices=NEED_EXP, label='Requared work experience')
    employment = forms.MultipleChoiceField(
        choices=EMPLOYMENT, widget=forms.CheckboxSelectMultiple(), label='Employment type'
    )
    schedule = forms.MultipleChoiceField(
        choices=SCHEDULE, widget=forms.CheckboxSelectMultiple(), label='Work schedule'
    )
        
    class Meta:
        model = Vacancy
        fields = ('active', 'position', 'need_exp', 'employment', 'schedule', 'salary', 'body')


# PASSWORD 

class AuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='', widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Email'})
    )
    password = forms.CharField(
        label='', strip=False, min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='', strip=False, min_length=8, widget=forms.PasswordInput(
            attrs={'autofocus': True, 'placeholder': 'Old password'}
            )
    )
    new_password1 = forms.CharField(
        label='', strip=False, min_length=8, widget=forms.PasswordInput(
            attrs={'placeholder': 'New password'}
        )
    )
    new_password2 = forms.CharField(
        label='', strip=False, min_length=8, widget=forms.PasswordInput(
            attrs={'placeholder': 'New password again'}
        )
    )


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))


class PasswordSetForm(SetPasswordForm):
    password1 = forms.CharField(
        label='New password', strip=False, min_length=8, widget=forms.PasswordInput(
            attrs={'placeholder': 'New password'}
        )
    )
    password2 = forms.CharField(
        label='New password again', strip=False, min_length=8, widget=forms.PasswordInput(
            attrs={'placeholder': 'New password'}
        )
    )

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        password_validation.validate_password(password2)
        return password2
