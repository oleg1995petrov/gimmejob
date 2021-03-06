from django.db.models import Count

from .models import Vacancy
from . import choices


class VacancyFilterMixin:
    # def get_published(self):
    #     return Vacancy.objects.filter(active=True).values('published')

    # def get_experience(self):
    #     return Vacancy.objects.filter(active=True).values('experience').annotate(count=Count('experience')).order_by('count')

    # def get_employment(self):
    #     return Vacancy.objects.filter(active=True).values('employment').annotate(count=Count('employment')).order_by('count')

    # def get_schedule(self):
    #     return Vacancy.objects.filter(active=True).values('schedule').annotate(count=Count('schedule')).order_by('count')

    # def get_salary(self):
    #     return Vacancy.objects.filter(active=True).values('salary').annotate(count=Count('salary')).order_by('count')

    def get_vacancy_experience(self):
        EXPERIENCE = {}
        for i in choices.EXPERIENCE:
            EXPERIENCE[i[1]] = i[0]

        return EXPERIENCE
    
    def get_vacancy_employment(self):
        EMPLOYMENT = {}
        for i in choices.EMPLOYMENT:
            EMPLOYMENT[i[1]] = i[0]

        return EMPLOYMENT

    def get_vacancy_schedule(self):
        SCHEDULE = {}
        for i in choices.SCHEDULE:
            SCHEDULE[i[1]] = i[0]

        return SCHEDULE
