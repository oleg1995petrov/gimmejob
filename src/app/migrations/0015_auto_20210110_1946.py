# Generated by Django 3.1.4 on 2021-01-10 16:46

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20210110_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='education',
            field=models.CharField(blank=True, choices=[('SE', 'Secondary education'), ('AD', 'Associate’s degree'), ('BD', 'Bachelor’s degree'), ('MD', 'Master’s degree'), ('DD', 'Doctoral degree')], default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('RU', 'Russian'), ('BY', 'Belorussian'), ('EN', 'English'), ('UA', 'Ukrainian'), ('LV', 'Lithuanian'), ('LT', 'Latvian'), ('PL', 'Polish'), ('EE', 'Estonian'), ('DE', 'German'), ('FR', 'French'), ('ES', 'Spanish'), ('CH', 'Chinese'), ('JP', 'Japanese')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], default='', max_length=6),
        ),
        migrations.AlterField(
            model_name='profile',
            name='skills',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Driving Licence B', 'Driving Licence B'), ('Stress tolerance', 'Strees Tolerance'), ('MS Office', 'Ms Office'), ('Grammatically correct speech', 'Grammatically Correct Speech'), ('Teamwork', 'Teamwork'), ('Literacy', 'Literacy'), ('Corporate ethics', 'Corporate Ethics'), ('Negotiation', 'Negotiation')], max_length=50, null=True),
        ),
    ]