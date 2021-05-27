# Generated by Django 3.1.4 on 2021-01-14 00:12

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20210114_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='birthday',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='citizenship',
            field=models.CharField(choices=[('Republic of Belarus', 'Republic of Belarus'), ('Russian Federation', 'Russian Federation'), ('Ukraine', 'Ukraine'), ('Republic of Lithuania', 'Republic of Lithuania'), ('Republic of Latvia', 'Republic of Latvia'), ('Republic of Poland', 'Republic of Poland'), ('Republic of Estonia', 'Republic of Estonia')], default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='education',
            field=models.CharField(choices=[('high school', 'Hight school diploma'), ('associate', 'Associate’s degree'), ('bachelor', 'Bachelor’s degree'), ('master', 'Master’s degree'), ('doctoral', 'Doctoral degree')], default='', max_length=11),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('russian', 'Russian'), ('belarussian', 'Belorussian'), ('english', 'English'), ('ukrainian', 'Ukrainian'), ('lithuanian', 'Lithuanian'), ('latvian', 'Latvian'), ('polish', 'Polish'), ('estonian', 'Estonian'), ('german', 'German'), ('french', 'French'), ('spanish', 'Spanish'), ('chinese', 'Chinese'), ('japanese', 'Japanese')], max_length=111, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='location',
            field=models.CharField(choices=[('Belarus', (('Brest', 'Brest'), ('Grodno', 'Grodno'), ('Gomel', 'Gomel'), ('Minsk', 'Minsk'), ('Mogilev', 'Mogilev'), ('Vitebsk', 'Vitebsk'))), ('Russia', (('Moscow', 'Moscow'),)), ('Poland', (('Warsaw', 'Warsaw'),)), ('Ukraine', (('Kiev', 'Kiev'),)), ('Lithuania', (('Vilnius', 'Vilnius'),)), ('Latvia', (('Riga', 'Riga'),)), ('Estonia', (('Tallinn', 'Tallinn'),))], default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='photo',
            field=models.ImageField(upload_to='applicants/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='specialization',
            field=models.CharField(choices=[('economist', 'Economist'), ('lawyer', 'Lawyer'), ('engineer', 'Engineer'), ('architect', 'Architect'), ('teacher', 'Teacher'), ('driver', 'Driver'), ('cook', 'Cook'), ('seller', 'Seller'), ('manager', 'Manager')], default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='employeer',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='employeer',
            name='info',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='employeer',
            name='photo',
            field=models.ImageField(upload_to='employeers/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='employeer',
            name='site',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='experience',
            name='company_site',
            field=models.URLField(null=True),
        ),
    ]
