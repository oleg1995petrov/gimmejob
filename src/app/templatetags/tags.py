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

    now = exp.now
    if now:
        month_now = date.today().month
        year_now = date.today().year

    end = exp.end
    if end:
        month_end = end.month
        year_end = end.year

    if now:
        num_calendar_years = year_now - year_begin
    else:
        num_calendar_years = year_end - year_begin

    if not num_calendar_years:
        if now:
            num_months = month_now - month_begin + 1
        else:
            num_months = month_end - month_begin + 1
    else:
        if now:
            num_months = month_now + num_calendar_years * 12 + 1 - month_begin
        else:
            num_months = month_end + num_calendar_years * 12 + 1 - month_begin

    years = num_months // 12
    months = num_months % 12

    if years:
        res = f'{years} г. {months} мес.'
    else:
        res = f'{months} мес.'
    return res



# @register.simple_tag
# @register.inclusion_tag
