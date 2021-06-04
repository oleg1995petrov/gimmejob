from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AbstractUser, PermissionsMixin
from django.conf import settings
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.fields.related_descriptors import ManyToManyDescriptor
from django.forms.widgets import NumberInput
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.urls import reverse


from datetime import date

from multiselectfield.utils import get_max_length
from . import choices
from . import services


class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name='', last_name='', company=''):
        user = self.model(
            first_name=first_name, 
            last_name=last_name, 
            email=self.normalize_email(email), 
            company=company
        )
        user.set_password(password)
        user.save(using=self._db)
        return user 

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email), 
            password=password
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField('Имя', max_length=255, default='')
    last_name = models.CharField('Фамилия', max_length=255, default='')
    email = models.EmailField('Электронный адрес', max_length=255, unique=True)
    company = models.CharField('Организация', max_length=100, default='')
    #user_type = models.CharField('Тип пользователя', max_length=15, default='')
    is_active = models.BooleanField('Активная учетная запись', default=True)
    is_admin = models.BooleanField('Админ', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_employer(self):
        if self.company:
            return True
        return False
 
    @property
    def is_applicant(self):
        return not self.is_employer

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.id})


class Applicant(models.Model):

    MAX_PHOTO_SIZE = 3145728

    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='applicant')
    photo = models.ImageField('Фото', upload_to=services.rename_avatar, null=True, blank=True)
    birthday = models.DateField('Дата рождения', null=True, blank=True)
    location = models.CharField('Город проживания', max_length=50, choices=choices.LOCATION, default='',)
    citizenship = models.CharField('Гражданство', max_length=50, choices=choices.COUNTRIES, default='')
    languages = ManyToManyField('Language', through='ApplicantLanguage', verbose_name='Языки', related_name='applicant')

    class Meta:
        verbose_name = 'Соискаитель'
        verbose_name_plural = 'Соискаители'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.user.id})


class Employer(models.Model):

    MAX_PHOTO_SIZE = 1048576
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='employer')
    photo = models.ImageField('Фото', upload_to=services.rename_avatar, null=True, blank=True)
    company_email = models.EmailField('Корпоративная почта', null=True)
    company_site = models.URLField('Корпоративный сайт', null=True)
    company_info = models.TextField('Об организации', default='')
    company_spheres = MultiSelectField('Сфера деятельности компании', choices=choices.SPHERES, null=True)

    class Meta:
        verbose_name = 'Работодатель'
        verbose_name_plural = 'Работодатели'

    def __str__(self):
        return self.user.company
            
    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.user.id})

### LANGUAGE

class Language(models.Model):

    language = models.CharField('Язык', max_length=50)
    level = models.CharField('Уровень владения', max_length=25, null=True, blank=True)

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'

    def __str__(self):
        if self.level:
            return f'{self.language} ({self.level})'
        else:
            return f'{self.language}'
        

class ApplicantLanguage(models.Model):

    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

### LANGUAGE


class Education(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, verbose_name='Соискатель', related_name='education')
    institution = models.CharField('Уч. заведение', max_length=200, default='')
    degree = models.CharField('Степень', max_length=100, default='', blank=True)
    specialization = models.CharField('Специализация', max_length=100, default='', blank=True)
    year_start = models.DateField('Год начала', null=True, blank=True)
    year_end = models.DateField('Год окончания (или ожидаемый)', null=True, blank=True)
    description = models.CharField('Описание', max_length=2000, default='', blank=True)    

    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образование'
        ordering = ['-year_end', '-year_start', '-id']


class Experience(models.Model):
    """ """

    applicant = models.ForeignKey(Applicant, verbose_name='Соискатель', on_delete=models.CASCADE, related_name='experience')
    position = models.CharField('Должность', max_length=100, default='')
    employment = models.CharField('Тип занятости', max_length=50, choices=choices.EMPLOYMENT, default='', blank=True)
    company = models.CharField('Компания', max_length=100, default='')
    begin = models.DateField('С')
    end = models.DateField('По', null=True, blank=True)
    description = models.CharField('Описание', max_length=2000, default='', blank=True)
    
    class Meta:
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыт работы'
        ordering = ['-end', '-begin', '-id']

    def __str__(self):
        return f'Experience of Applicant-{self.applicant.id}'
        
    @property
    def get_employment(self):
        if self.employment == 'ftime':
            return 'Полная занятость'
        elif self.employment == 'ptime':
            return 'Частичная занятость'
        elif self.employment == 'trainee':
            return 'Стажировка'
        elif self.employment == 'profedu':
            return 'Профессиональное обучение'
        elif self.employment == 'business':
            return 'Предприниматель'
        elif self.employment == 'free':
            return 'Фриланс'


class Vacancy(models.Model):
   
    employer = models.ForeignKey(
        Employer, 
        verbose_name='Работадатель',
        on_delete=models.CASCADE, 
        related_name='vacancies'
    )
    published = models.DateTimeField('Опубликовано', default=timezone.now)
    active = models.BooleanField('Публиковать?')
    position = models.CharField('Должность', max_length=100)
    experience = models.CharField('Требуемый опыт работы', max_length=50, choices=choices.EXPERIENCE)
    employment = MultiSelectField('Тип занятости', max_length=100, choices=choices.EMPLOYMENT)
    schedule = MultiSelectField('График работы', max_length=100, choices=choices.SCHEDULE)
    salary = models.PositiveSmallIntegerField('Уровень дохода', null=True)
    currency = models.CharField('Валюта', max_length=3, choices=choices.CURRENCIES, default='')
    body = models.TextField('Описание вакансии')
    
    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-published']
    
    def __str__(self):
        return f'{self.employer.user.company} {self.position}'
    
    def get_absolute_url(self):
        return reverse('vacancy_detail', kwargs={'vacancy_id': self.id})
        
    @property
    def is_active(self):
        return self.active    

    def get_short_body(self):
        raw = list(self.body[:450])
        clear = []
        flag = True

        for i in raw:
            if i in '<&':
                flag = False
                continue
            elif i in '>;':
                flag = True
                continue
            if i not in '<>' and flag:
                clear.append(i)

        return f"{''.join(clear)} ..."
