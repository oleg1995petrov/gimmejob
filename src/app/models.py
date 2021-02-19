from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AbstractUser, PermissionsMixin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from multiselectfield import MultiSelectField

from datetime import date
from .choices import *


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password, company=None):
        user = self.model(
            first_name=first_name, 
            last_name=last_name, 
            email=self.normalize_email(email), 
            company=company
        )
        user.set_password(password)
        user.save(using=self._db)
        return user 

    def create_superuser(self, email, password, first_name=None, last_name=None):
        user = self.create_user(
            first_name=first_name, 
            last_name=last_name, 
            email=self.normalize_email(email), 
            password=password
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    company = models.CharField(max_length=100, default='')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Applicant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applicant')
    photo = models.ImageField(upload_to='applicants/%Y/%m/%d')
    birthday = models.DateField(null=True)
    location = models.CharField(max_length=50, choices=LOCATION, default='')
    citizenship = models.CharField(max_length=50, choices=COUNTRIES, default='')
    education = models.CharField(max_length=11, choices=EDUCATION, default='')
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION, default='')
    skills = MultiSelectField(choices=SKILLS, blank=True, null=True)
    languages = MultiSelectField(choices=LANGUAGES, null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} Applicant Profile'


class Employer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employer')
    photo = models.ImageField(upload_to='employers/%Y/%m/%d')
    company_email = models.EmailField(null=True)
    company_site = models.URLField(null=True)
    company_info = models.TextField(
        default='Something about the company. History, goals, missions, values, features, advantages, etc.'
    )
    company_spheres = MultiSelectField(choices=SPHERES, null=True)

    def __str__(self):
        return f'{self.user.company} Employer Profile'


class Experience(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='experience')
    begin = models.DateField()
    now = models.BooleanField(null=True)
    end = models.DateField(null=True)
    company = models.CharField(max_length=100)
    company_site = models.URLField(null=True)
    company_spheres = MultiSelectField(choices=SPHERES)
    position = models.CharField(max_length=50)
    responsibilities = models.TextField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.applicant.user.first_name} {self.applicant.user.last_name} Experience'


class Vacancy(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='vacancies')
    published = models.DateTimeField(default=timezone.now)
    active = models.BooleanField()
    position = models.CharField(max_length=100)
    need_exp = models.CharField(max_length=50, choices=NEED_EXP)
    employment = MultiSelectField(max_length=100, choices=EMPLOYMENT)
    schedule = MultiSelectField(max_length=100, choices=SCHEDULE)
    salary = models.PositiveSmallIntegerField(null=True)
    body = models.TextField()
    
    class Meta:
        ordering = ['-published']

    def __str__(self):
        return f'{self.employer.user.company} {self.position}'
