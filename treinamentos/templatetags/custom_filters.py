from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    """ Substitui espaços por hífens ou qualquer outro caractere """
    return value.replace(" ", arg)