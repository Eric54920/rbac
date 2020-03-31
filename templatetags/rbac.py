from django import template
from django.conf import settings
from collections import OrderedDict
import re

register = template.Library()

@register.inclusion_tag('menu.html')
def menu(request):
    url = request.path_info
    # 排序
    orderdict = OrderedDict()
    menu_dic = request.session.get(settings.MENU_SESSION_KEY)
    for key in sorted(menu_dic, key=lambda x: menu_dic[x]['weight'], reverse=True):
        orderdict[key] = menu_dic[key]

    # 对当前所在页面加样式
    for i in orderdict.values():
        i['class'] = 'hidden'
        for child in i['children']:
            if child['id'] == request.current_menu_id:
                child['class'] = 'active'
                i['class'] = ''

    return {'orderdict': orderdict.values()}

@register.inclusion_tag('breadcrumb.html')
def breadcrumb(request):
    url = request.path_info
    permission = request.session.get(settings.PERMISSION_SESSION_KEY)
    breadcrumb = []
    for i in permission.values():
        if url == i['url']:
            breadcrumb.append({'name': i['name'], 'url': i['url']})
            if i['pid']:
                parent = permission[i['title']]
                breadcrumb.append({'name': parent['name'], 'url': parent['url']})
            break
    return {'breadcrumb':breadcrumb}

@register.filter()
def has_permission(request, name): 
    if name in request.session.get(settings.PERMISSION_SESSION_KEY):
        return True
    else:
        return False

