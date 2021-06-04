import abc
from django.template import Library
from django.conf import settings

from datetime import date

from app import services


register = Library()


@register.inclusion_tag('filters/footer.html')
def get_footer():
    current_year = date.today().year
    return {'current_year': current_year}


@register.inclusion_tag('filters/messages.html', takes_context=True)
def get_messages(context):
    messages = context['messages']
    return {'messages': messages}


@register.simple_tag
def get_work_period(exp):
    begin = exp.begin
    begin_month = begin.month
    begin_year = begin.year
    end = exp.end

    if end:
        month_end = end.month
        year_end = end.year
    else:
        month_end = date.today().month
        year_end = date.today().year

    num_years = year_end - begin_year
    num_months = (month_end - begin_month) + 1

    if num_years:
        num_months += num_years * 12

    years = num_months // 12
    months = num_months % 12

    if years and months:
        res = f'{services.get_year_ending(years)} {months} мес.'
    elif years:
        res = f'{services.get_year_ending(years)} {months} мес.'
    else:
        res = f'{months} мес.'
    return res



# @register.simple_tag
# @register.inclusion_tag
