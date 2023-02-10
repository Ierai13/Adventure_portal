from django import template


register = template.Library()


@register.filter()
def cat_translate(category):
    TRANS = {
        'Tanks': 'Танки',
        'Healers': 'Хилы',
        'DD': 'ДД',
        'Traders': 'Торговцы',
        'GMs': 'Гилдмастеры',
        'QGs': 'Квестгиверы',
        'Blacksmiths': 'Кузнецы',
        'Leatherworkers': 'Кожевники',
        'Potionmaker': 'Зельевары',
        'SM': 'Мастера заклинаний'
    }
    if category in TRANS.keys():
        category = TRANS[category]
        return category


@register.filter()
def confirmation(value):
    if value:
        return 'Приняли'
    else:
        return 'Отклонили'
