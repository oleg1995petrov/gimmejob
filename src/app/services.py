from django.core.mail import send_mail
from django.conf import settings


def is_true_period(datadict):
    """Checking if the work experience period is true"""

    begin, now, end = datadict['begin'], datadict['now'], datadict['end']
    return (begin and end and not now and end >= begin) or (begin and not end and now)


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
