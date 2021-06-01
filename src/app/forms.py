from django import forms
from django.contrib.auth import load_backend, login, password_validation
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField, PasswordChangeForm, SetPasswordForm, 
    UserCreationForm, AuthenticationForm, PasswordResetForm
)
from ckeditor.widgets import CKEditorWidget

from PIL import Image
import os
from django.forms import fields

from django.http import request
from django.forms.utils import ErrorDict

from . import services, choices
from .models import User, Applicant, Employer, Education, Experience, Vacancy, Language, ApplicantLanguage
from .widgets import MonthYearWidget, YearWidget



# help_text=password_validation.password_validators_help_text_html())

class ClearableFileInput(forms.ClearableFileInput):
    template_name = 'widgets/clearablefileinput.html'


# APPLICANT

class ApplicantCreationForm(forms.ModelForm):
    first_name = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Last name'})
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
        # fields = ('email',)

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
    first_name = forms.CharField(
        label='Имя:', 
        widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(
        label='Фамилия:', 
        widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(
        label='Электронный адрес:', 
        widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    
    def clean(self):
        cd = super().clean()
        errors = []
        fn = cd.get('first_name')
        ln = cd.get('last_name')

        if not fn.isalpha():
            errors.append(forms.ValidationError('Имя может содержать только буквы.'))

        if not ln.isalpha():
            errors.append(forms.ValidationError('Фамилия может содержать только буквы.'))
        
        if errors:
            raise forms.ValidationError([errors])


class ApplicantProfileForm(forms.ModelForm):
    birthday = forms.DateField(
        label='День рождения:',
        widget=forms.SelectDateWidget(years=choices.YEARS),
        required=False
    ) 
    location = forms.CharField(
        label='Город',
        widget=forms.Select(choices=choices.LOCATION),
        required=False
    )
    citizenship = forms.CharField(
        label='Гражданство',
        widget=forms.Select(choices=choices.COUNTRIES),
        required=False
    )

    class Meta:
        model = Applicant
        fields = ('birthday', 'location', 'citizenship')      


class PhotoForm(forms.ModelForm):
    photo = forms.ImageField(
        label='',
        required=False, 
        widget=ClearableFileInput()
    )

    class Meta:
        model = Applicant
        fields = ('photo',)

    def clean(self):
        cd = super().clean()
        photo = cd['photo']
        
        if photo:
            if photo.size > Applicant.MAX_PHOTO_SIZE:
                raise forms.ValidationError('Слишком большой вес изображения!')

        if self.has_changed():
            if ('photo' in self.changed_data) or (photo == False and self.instance.photo):
                # if os.path.isfile(self.instance.photo.path):
                self.instance.photo.delete()
    

class EducationForm(forms.ModelForm):
    education = forms.CharField(label='Степень *', widget=forms.Select(choices=choices.DEGREE), required=False)
    specialization = forms.CharField(label='Специализация', widget=forms.Select(choices=choices.SPECIALIZATION), required=False)

    class Meta:
        model = Applicant
        fields = ('education', 'specialization')


class EduForm(forms.ModelForm):

    universiry = forms.CharField(label="Уч. заведение")
    degree = forms.CharField(label="Степень", widget=forms.Select(choices=choices.DEGREE), required=False)
    specialization = forms.CharField(label="Специализация", widget=forms.Select(choices=choices.SPECIALIZATION), required=False)
    year_start = forms.DateField(label='Год начала', widget=YearWidget(years=choices.WORK_YEARS), required=False)
    year_end = forms.DateField(label='Год окончания ', widget=YearWidget(years=choices.WORK_YEARS), required=False)
    description = forms.CharField(label="Описание", widget=forms.Textarea(), required=False)

    class Meta:
        model = Education
        exclude = ('applicant',)
   

class ExperienceForm(forms.ModelForm):
   
    position = forms.CharField(label="Должность *")
    employment = forms.CharField(label='Тип занятости', widget=forms.Select(choices=choices.EMPLOYMENT), required=False)
    company = forms.CharField(label='Компания *')
    begin = forms.DateField(label='Дата начала *', widget=MonthYearWidget(years=choices.WORK_YEARS), required=False)
    end = forms.DateField(label='Дата окончания', widget=MonthYearWidget(years=choices.WORK_YEARS), required=False)
    description = forms.CharField(label='Описание', widget=forms.Textarea(), required=False)
    
    class Meta:
        model = Experience
        exclude = ('applicant',)

    def clean(self):
        cd = super().clean()
        self._errors = ErrorDict()
        begin = cd.get('begin')
        end = cd.get('end')
    
        if not begin:
            self.add_error('begin', 'Заполните поле "Дата начала"')
            return
        
        if end and begin > end:
            self.add_error('end', 'Укажите правильный временной период')
            

class SkillsForm(forms.ModelForm):
    skills = forms.MultipleChoiceField(
        label='',
        required=False,
        choices=choices.SKILLS,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Applicant
        fields = ('skills',)


class LanguageForm(forms.ModelForm):
       
    language = forms.CharField(
        widget=forms.Select(choices=choices.LANGUAGES),
        label='Язык'
    )
    level = forms.CharField(
        widget=forms.Select(choices=choices.LANGUAGE_LEVELS),
        label='Уровень знания',
        required=False
    )
            
    class Meta:
        model = Language
        fields = '__all__'
   

# EMPLOYEER 
class EmployerCreationForm(forms.ModelForm):
    # first_name = forms.CharField(
    #     label='', widget=forms.TextInput(attrs={'autofocus': True,'placeholder': 'First name'})
    # )
    # last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(
        label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    company = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Company'}))
    password1 = forms.CharField(
        label='', 
        strip=False, 
        min_length=8, 
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}
        )
    )
    password2 = forms.CharField(
        label='', 
        strip=False, 
        min_length=8, 
        widget=forms.PasswordInput(attrs={'placeholder': 'Password again'})
    )

    class Meta:
        model = User
        # fields = ('first_name', 'last_name', 'email', 'company')
        fields = ('email', 'company')


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
    first_name = forms.CharField(
        label='', 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(
        label='',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(
        label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Personal email'}))
    company = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Company name'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'company')


class EmployerProfileForm(forms.ModelForm):
    photo = forms.ImageField(
        label='',
        required=False,
        widget=ClearableFileInput()
    )
    company_email = forms.EmailField(
        required=False, 
        label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Company email'})
    )
    company_site = forms.URLField(
        required=False, 
        label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Company website: http://'})
    )
    company_info = forms.CharField(
        required=False, 
        label='About the company', 
        widget=CKEditorWidget()
    )
    company_spheres = forms.MultipleChoiceField(
        required=True, 
        label='Company scopes',
        choices=choices.SPHERES,
        widget=forms.CheckboxSelectMultiple(), 
    )

    class Meta:
        model = Employer
        fields = ('photo', 'company_email', 'company_site', 'company_info', 'company_spheres')

    def clean(self):
        cleaned_data = super().clean()
        photo = cleaned_data['photo']
        min_coef = 0.9
        max_coef = 1.1

        if photo:
            pht = Image.open(photo)
            width, height = pht.width, pht.height
            coef = width / height

            if photo.size > Employer.MAX_PHOTO_SIZE:
                raise forms.ValidationError('Максимальный размер логотипа - 1 мегабайт!')
            if coef < min_coef or coef > max_coef:
                raise forms.ValidationError('Логотип должен быть квадратной формы!')

        if self.has_changed():
            if 'photo' in self.changed_data or photo == False and self.instance.photo:
                # if os.path.isfile(self.instance.photo.path):
                self.instance.photo.delete()


class VacancyForm(forms.ModelForm):
    salary = forms.IntegerField(required=False, min_value=0, label='Уровень оплаты')
    currency = forms.ChoiceField(choices=choices.CURRENCIES, label='Валюта', required=False)
    body = forms.CharField(widget=CKEditorWidget(), label='Описание вакансии')
    # schedule = forms.ChoiceField(choices=Vacancy.VacancySchedule.choices, widget=forms.CheckboxSelectMultiple(), label='Валюта', required=False)
    
    class Meta:
        model = Vacancy
        fields = ('active', 'position', 'experience', 'employment', 'schedule', 'salary', 'currency', 'body')


# PASSWORD 

class AuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='', 
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Email'})
    )
    password = forms.CharField(
        label='', 
        strip=False, 
        min_length=8, 
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='', 
        strip=False, 
        min_length=8, 
        widget=forms.PasswordInput(attrs={'autofocus': True, 'placeholder': 'Old password'})
    )
    new_password1 = forms.CharField(
        label='', 
        strip=False, 
        min_length=8, 
        widget=forms.PasswordInput(attrs={'placeholder': 'New password'}
        )
    )
    new_password2 = forms.CharField(
        label='', 
        strip=False, 
        min_length=8, 
        widget=forms.PasswordInput(attrs={'placeholder': 'New password again'}
        )
    )


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Email'}))


class PasswordSetForm(SetPasswordForm):
    password1 = forms.CharField(
        label='New password', 
        strip=False, 
        min_length=8, 
        widget=forms.PasswordInput(attrs={'placeholder': 'New password'})
    )
    password2 = forms.CharField(
        label='New password again', 
        strip=False, 
        min_length=8, 
        widget=forms.PasswordInput(attrs={'placeholder': 'New password'}
        )
    )

    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'])
        password_validation.validate_password(password2)
        return password2
