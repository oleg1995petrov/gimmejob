from django.core.mail import send_mail
from django.conf import settings
import os

from . import models

def send_mail_registration(user):
    if user.company:
        usr = 'employer'
    else:
        usr = 'applicant'

    return send_mail(
        "GimmeJob | Successful registration",
        f'Dear {usr}, welcome to GimmeJob!',
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False)


def rename_avatar(instance, filename):
    ext = filename.split('.')[-1]
    path = f'users/{instance.user.id}'
    name = f'{instance.user.id}.{ext}'
    return os.path.join(path, name)


def get_next_path(request):
    return f'?next={request.get_full_path()}'

# def get_vacancy_experience():
#     experience = {}
#     for i in models.Vacancy.EXPERIENCE:
#         experience[i[1]] = i[0]

#     return experience
