from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()


@register.filter(is_safe=True)
@stringfilter
def only_first_period(value, delimiter=None):
    return value.split(delimiter)[0]


# @register.simple_tag
# @register.inclusion_tag