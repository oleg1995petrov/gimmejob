from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()


@register.filter(is_safe=True)
@stringfilter
def only_first_period(dt, delimiter=','):
    return dt.split(delimiter)[0]


# @register.simple_tag
# @register.inclusion_tag