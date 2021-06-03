import abc
from django.template import Library
from django.conf import settings

from datetime import date


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
    month_begin = begin.month
    year_begin = begin.year
    end = exp.end

    if end:
        month_end = end.month
        year_end = end.year
    else:
        month_end = date.today().month
        year_end = date.today().year

    num_years = year_end - year_begin
    num_months = (month_end - month_begin) + 1

    if num_years:
        num_months += num_years * 12

    years = num_months // 12
    months = num_months % 12

    if years and months:
        res = f'{years} г. {months} мес.'
    elif years:
        if years % 10 in [1, 2, 3, 4] and years not in [11, 12, 13, 14]:
            res = f'{years} г'
        else:
            res = f'{years} л'
    else:
        res = f'{months} мес.'
    return res



# @register.simple_tag
# @register.inclusion_tag
