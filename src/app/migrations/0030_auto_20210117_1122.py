# Generated by Django 3.1.4 on 2021-01-17 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_vacancy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='position',
            field=models.CharField(max_length=50),
        ),
        migrations.DeleteModel(
            name='Vacancy',
        ),
    ]