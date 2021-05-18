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




# @register.simple_tag
# @register.inclusion_tag
