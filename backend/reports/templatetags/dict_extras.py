from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Permet d'accéder à dictionary[key]"""
    return dictionary.get(key)

@register.filter
def dictkey(dictionary, key):
    """Accède à une clé de dictionnaire dans un template"""
    try:
        return dictionary[key]
    except (KeyError, TypeError):
        return None
