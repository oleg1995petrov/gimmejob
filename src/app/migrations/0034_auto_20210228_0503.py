# Generated by Django 3.1.6 on 2021-02-28 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_auto_20210214_0428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='education',
            field=models.CharField(choices=[(None, '------------'), ('High school', 'Hight school diploma'), ("Associate's", 'Associate’s'), ("Bachelor's", 'Bachelor’s'), ("Master's", 'Master’s'), ('Doctoral', 'Doctoral')], default='', max_length=11),
        ),
    ]
