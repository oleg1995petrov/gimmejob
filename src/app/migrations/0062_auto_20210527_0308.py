# Generated by Django 3.1.6 on 2021-05-27 00:08

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0061_auto_20210526_0613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='education',
            field=models.CharField(choices=[(None, '------------'), ('High School Diploma', 'High school diploma'), ('Associate degree', 'Associate’s degree'), ('Бакалавр', 'Бакалавр'), ('Мастер', 'Мастер'), ('Доктор', 'Доктор')], default='', max_length=20, verbose_name='Уровень образования'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='specialization',
            field=models.CharField(choices=[(None, '------------'), ('Экономист', 'Экономист'), ('Lawyer', 'Lawyer'), ('Инженер', 'Инженер'), ('Architect', 'Architect'), ('Teacher', 'Teacher'), ('Driver', 'Driver'), ('Cook', 'Cook'), ('Seller', 'Seller'), ('Manager', 'Manager')], default='', max_length=50, verbose_name='Специализация'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='currency',
            field=models.CharField(choices=[(None, '-'), ('BYN', 'BYN'), ('RUB', 'RUB'), ('USD', 'USD'), ('EUR', 'EUR')], default='', max_length=3, verbose_name='Валюта'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='employment',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('ftime', 'Полная занятость'), ('ptime', 'Частичная занятость'), ('trainee', 'Стажировка'), ('profedu', 'Профессиональное обучение'), ('business', 'Предприниматель'), ('free', 'Фриланс')], max_length=100, verbose_name='Тип занятости'),
        ),
    ]
