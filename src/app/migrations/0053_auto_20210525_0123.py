# Generated by Django 3.1.6 on 2021-05-24 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0052_auto_20210524_2256'),
    ]

    operations = [
        migrations.CreateModel(
            name='LanguageLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=50, verbose_name='Язык')),
                ('level', models.CharField(max_length=25, verbose_name='Уровень владения')),
            ],
            options={
                'verbose_name': 'Язык и уровень его знания',
                'verbose_name_plural': 'Языки и уровни их знаний',
            },
        ),
        migrations.AddField(
            model_name='applicant',
            name='languages',
            field=models.ManyToManyField(related_name='applicant', to='app.LanguageLevel', verbose_name='Языки'),
        ),
    ]