from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    """ Substitui espaços por um caractere definido (ex: '-' para uso em IDs) """
    return value.replace(" ", arg)
