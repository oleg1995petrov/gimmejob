from django.core.mail import send_mail
from django.conf import settings
import os

from django.http import request
from django.contrib import messages
from django.utils.safestring import mark_safe

from . import models, choices


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


def get_languages(applicant):
    LANGUAGES = choices.LANGUAGES 
    applicant_langs = [lang.language for lang in models.Language.objects.filter(applicant=applicant)]
    if applicant_langs:
        for _ in range(len(applicant_langs)):
            for lang in LANGUAGES:
                if lang[0] in applicant_langs:
                    LANGUAGES.remove(lang)
    
    return LANGUAGES


def message_succes(request, has_errors=False):
    if not has_errors:
        messages.success(
            request,
            mark_safe('<b>Изменения сохранены.</b><br>Ваш профиль был успешно обновлен.')
        )
