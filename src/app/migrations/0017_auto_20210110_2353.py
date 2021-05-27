# Generated by Django 3.1.4 on 2021-01-10 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20210110_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='citizenship',
            field=models.CharField(blank=True, choices=[('Republic of Belarus', 'Republic of Belarus'), ('Russian Federation', 'Russian Federation'), ('Ukraine', 'Ukraine'), ('Republic of Lithuania', 'Republic of Lithuania'), ('Republic of Latvia', 'Republic of Latvia'), ('Republic of Poland', 'Republic of Poland'), ('Republic of Estonia', 'Republic of Estonia')], default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='education',
            field=models.CharField(blank=True, choices=[('high school', 'Hight school diploma'), ('associate', 'Associate’s degree'), ('bachelor', 'Bachelor’s degree'), ('master', 'Master’s degree'), ('doctoral', 'Doctoral degree')], default='', max_length=11),
        ),
        migrations.AlterField(
            model_name='profile',
            name='specialization',
            field=models.CharField(blank=True, choices=[('economist', 'Economist'), ('lawyer', 'Lawyer'), ('engineer', 'Engineer'), ('architect', 'Architect'), ('teacher', 'Teacher'), ('driver', 'Driver'), ('cook', 'Cook'), ('seller', 'Seller'), ('manager', 'Manager')], default='', max_length=50),
        ),
    ]