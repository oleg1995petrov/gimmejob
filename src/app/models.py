from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AbstractUser, PermissionsMixin
from django.conf import settings
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
    email = models.EmailField('Электронная почта', max_length=255, unique=True)
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
    education = models.CharField('Уровень образования', max_length=20, choices=choices.EDUCATION, default='')
    specialization = models.CharField('Специализация', max_length=50, choices=choices.SPECIALIZATION, default='')
    skills = MultiSelectField('Ключевые навыки', max_length=1000, choices=choices.SKILLS, blank=True, null=True)
    languages = MultiSelectField('Знание языков', max_length=500, choices=choices.LANGUAGES, blank=True, null=True)

    class Meta:
        verbose_name = 'Соискаитель'
        verbose_name_plural = 'Соискаители'

    def __str__(self):
        return self.user.first_name, self.user.last_name
    
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
    

class Experience(models.Model):
    applicant = models.ForeignKey(Applicant, verbose_name='Соискатель', on_delete=models.CASCADE, related_name='experience')
    begin = models.DateField('Начало работы')
    now = models.BooleanField('По настоящее время', null=True)
    end = models.DateField('Окончание', null=True)
    company = models.CharField('Организация', max_length=100)
    company_site = models.URLField('Сайт', null=True)
    company_spheres = MultiSelectField('Сфера деятельности компании', choices=choices.SPHERES)
    position = models.CharField('Должность', max_length=50)
    responsibilities = models.TextField('Обязанности на рабочем месте')

    class Meta:
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыт работы'
        ordering = ['-id']

    def __str__(self):
        return f'Experience of Applicant-{self.applicant.id}'


class Vacancy(models.Model):
    EXPERIENCE = (
        ('noExp', _('Без опыта')),
        ('from1To3', _('От 1 года до 3 лет')),
        ('from3To6', _('От 3 до 6 лет')),
        ('over6', _('Более 6 лет'))
    )

    EMPLOYMENT = (
        ('ftime', _('Полная занятость')),
        ('ptime', _('Частичная занятость')),
        ('trainee', _('Стажировка'))
    )

    SCHEDULE = (
        ('fday', _('Полный день')),
        ('shift', _('Сменный график')),
        ('flex', _('Гибкий график')),
        ('remote', _('Удаленная работа'))
    )

    CURRENCY = (
        (None, '------------'),
        ('BYN', 'BYN'),
        ('RUB', 'RUB'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    )
   
    employer = models.ForeignKey(
        Employer, 
        verbose_name='Работадатель',
        on_delete=models.CASCADE, 
        related_name='vacancies'
    )
    published = models.DateTimeField('Опубликовано', default=timezone.now)
    active = models.BooleanField('Публиковать?')
    position = models.CharField('Должность', max_length=100)
    experience = models.CharField('Требуемый опыт работы', max_length=50, choices=EXPERIENCE)
    employment = MultiSelectField('Тип занятости',max_length=100, choices=EMPLOYMENT)
    schedule = MultiSelectField('График работы',max_length=100, choices=SCHEDULE)
    salary = models.PositiveSmallIntegerField('Уровень дохода', null=True)
    currency = models.CharField('Валюта',max_length=3, choices=CURRENCY, default='')
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
