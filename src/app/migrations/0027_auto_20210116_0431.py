# Generated by Django 3.1.4 on 2021-01-16 01:31

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20210115_2116'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeer',
            old_name='email',
            new_name='company_email',
        ),
        migrations.RenameField(
            model_name='employeer',
            old_name='info',
            new_name='company_info',
        ),
        migrations.RenameField(
            model_name='employeer',
            old_name='site',
            new_name='company_site',
        ),
        migrations.RenameField(
            model_name='employeer',
            old_name='spheres',
            new_name='company_spheres',
        ),
        migrations.AlterField(
            model_name='applicant',
            name='skills',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('driving_licence_b', 'Driving licence B'), ('strees_tolerance', 'Stress tolerance'), ('ms_office', 'MS Office'), ('grammatically_correct_speech', 'Grammatically correct speech'), ('teamwork', 'Teamwork'), ('literacy', 'Literacy'), ('corporate_ethics', 'Corporate ethics'), ('negotiation', 'Negotiation')], max_length=120, null=True),
        ),
    ]
