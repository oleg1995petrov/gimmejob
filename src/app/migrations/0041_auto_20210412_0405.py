# Generated by Django 3.1.6 on 2021-04-12 01:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_auto_20210405_0205'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='experience',
            options={'ordering': ['-id'], 'verbose_name': 'Опыт работы', 'verbose_name_plural': 'Опыт работы'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.RemoveField(
            model_name='vacancy',
            name='need_exp',
        ),
        migrations.AddField(
            model_name='vacancy',
            name='experience',
            field=models.CharField(choices=[('noExperience', 'Без опыта'), ('from1To3', 'От 1 года до 3 лет'), ('from3To6', 'От 3 до 6 лет'), ('over6', 'Более 6 лет')], default='noExperience', max_length=50, verbose_name='Требуемый опыт работы'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='birthday',
            field=models.DateField(null=True, verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='citizenship',
            field=models.CharField(choices=[(None, '------------'), ('Republic of Belarus', 'Republic of Belarus'), ('Russian Federation', 'Russian Federation'), ('Ukraine', 'Ukraine'), ('Republic of Lithuania', 'Republic of Lithuania'), ('Republic of Latvia', 'Republic of Latvia'), ('Republic of Poland', 'Republic of Poland'), ('Republic of Estonia', 'Republic of Estonia')], default='', max_length=50, verbose_name='Гражданство'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='education',
            field=models.CharField(choices=[(None, '------------'), ('High school', 'Hight school diploma'), ("Associate's", 'Associate’s'), ("Bachelor's", 'Bachelor’s'), ("Master's", 'Master’s'), ('Doctoral', 'Doctoral')], default='', max_length=20, verbose_name='Уровень образования'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Russian', 'Russian'), ('Belarussian', 'Belarussian'), ('English', 'English'), ('Ukrainian', 'Ukrainian'), ('Lithuanian', 'Lithuanian'), ('Latvian', 'Latvian'), ('Polish', 'Polish'), ('Estonian', 'Estonian'), ('German', 'German'), ('French', 'French'), ('Spanish', 'Spanish'), ('Chinese', 'Chinese'), ('Japanese', 'Japanese')], max_length=111, null=True, verbose_name='Знание языков'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='location',
            field=models.CharField(choices=[(None, '------------'), ('Belarus', (('Brest', 'Brest'), ('Grodno', 'Grodno'), ('Gomel', 'Gomel'), ('Minsk', 'Minsk'), ('Mogilev', 'Mogilev'), ('Vitebsk', 'Vitebsk'))), ('Russia', (('Moscow', 'Moscow'),)), ('Poland', (('Warsaw', 'Warsaw'),)), ('Ukraine', (('Kiev', 'Kiev'),)), ('Lithuania', (('Vilnius', 'Vilnius'),)), ('Latvia', (('Riga', 'Riga'),)), ('Estonia', (('Tallinn', 'Tallinn'),))], default='', max_length=50, verbose_name='Город проживания'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='photo',
            field=models.ImageField(upload_to='applicants/%Y/%m/%d', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='skills',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('driving licence B', 'Driving licence B'), ('strees_tolerance', 'Stress tolerance'), ('ms_office', 'MS Office'), ('grammatically_correct_speech', 'Grammatically correct speech'), ('teamwork', 'Teamwork'), ('literacy', 'Literacy'), ('corporate_ethics', 'Corporate ethics'), ('negotiation', 'Negotiation')], max_length=120, null=True, verbose_name='Ключевые навыки'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='specialization',
            field=models.CharField(choices=[(None, '------------'), ('Economist', 'Economist'), ('Lawyer', 'Lawyer'), ('Engineer', 'Engineer'), ('Architect', 'Architect'), ('Teacher', 'Teacher'), ('Driver', 'Driver'), ('Cook', 'Cook'), ('Seller', 'Seller'), ('Manager', 'Manager')], default='', max_length=50, verbose_name='Специализация'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='applicant', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='employer',
            name='company_email',
            field=models.EmailField(max_length=254, null=True, verbose_name='Корпоративная почта'),
        ),
        migrations.AlterField(
            model_name='employer',
            name='company_info',
            field=models.TextField(default='', verbose_name='Об организации'),
        ),
        migrations.AlterField(
            model_name='employer',
            name='company_site',
            field=models.URLField(null=True, verbose_name='Корпоративный сайт'),
        ),
        migrations.AlterField(
            model_name='employer',
            name='company_spheres',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Energetics', 'Energetics'), ('Financial_sector', 'Financial sector'), ('Chemical_industry', 'The chemical industry'), ('Art and culture', 'Art and culture'), ('Education', 'Education'), ('Medecine', 'Medicine'), ('Retail', 'Retail'), ('Car_business', 'Car business'), ('IT', 'IT')], max_length=103, null=True, verbose_name='Сфера деятельности компании'),
        ),
        migrations.AlterField(
            model_name='employer',
            name='photo',
            field=models.ImageField(upload_to='employers/%Y/%m/%d', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='employer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employer', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experience', to='app.applicant', verbose_name='Соискатель'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='begin',
            field=models.DateField(verbose_name='Начало работы'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='company',
            field=models.CharField(max_length=100, verbose_name='Организация'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='company_site',
            field=models.URLField(null=True, verbose_name='Сайт'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='company_spheres',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Energetics', 'Energetics'), ('Financial_sector', 'Financial sector'), ('Chemical_industry', 'The chemical industry'), ('Art and culture', 'Art and culture'), ('Education', 'Education'), ('Medecine', 'Medicine'), ('Retail', 'Retail'), ('Car_business', 'Car business'), ('IT', 'IT')], max_length=103, verbose_name='Сфера деятельности компании'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='end',
            field=models.DateField(null=True, verbose_name='Окончание'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='now',
            field=models.BooleanField(null=True, verbose_name='По настоящее время'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='position',
            field=models.CharField(max_length=50, verbose_name='Должность'),
        ),
        migrations.AlterField(
            model_name='experience',
            name='responsibilities',
            field=models.TextField(verbose_name='Обязанности на рабочем месте'),
        ),
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.CharField(default='', max_length=100, verbose_name='Организация'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='', max_length=255, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активная учетная запись'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='Админ'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='', max_length=255, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='body',
            field=models.TextField(verbose_name='Описание вакансии'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='salary',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Уровень дохода'),
        ),
    ]
