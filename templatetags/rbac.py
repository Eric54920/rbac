from django import template
from django.conf import settings
from collections import OrderedDict

register = template.Library()

@register.inclusion_tag('rbac/menu.html')
def menu(request):
    menu_dict = request.session.get(settings.MENU_SESSION_KEY)
    order_dict = OrderedDict()

    for key in sorted(menu_dict, key=lambda x:menu_dict[x]['weight'], reverse=True):
        order_dict[key] = menu_dict[key]

    url = request.path_info
    for i in order_dict.values():
        for j in i['children']:
            if j['url'] == url:
                j['class'] = 'active'
    return {'menu_dict': order_dict.values()}