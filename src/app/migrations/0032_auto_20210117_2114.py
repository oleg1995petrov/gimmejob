# Generated by Django 3.1.4 on 2021-01-17 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_vacancy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='need_exp',
            field=models.CharField(choices=[('not_required', 'No experience'), ('1-3_years', 'From 1 to 3 years'), ('1-6_years', 'From 3 to 6 years'), ('over_6_years', 'Over 6 years')], max_length=50),
        ),
    ]