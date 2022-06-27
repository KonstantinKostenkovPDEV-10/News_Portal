from django import template
from re import search

register = template.Library()
bad_words = {
    'неописуемое',
    'описано',
    'сфере',
    'Это',
}


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def check_words(value):
    for word in bad_words:
        value = value.replace(word, len(word) * '*')
    return f'{value}'
