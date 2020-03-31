from django.conf import settings

def service(request, obj):    
    permission = obj.role.filter(permission__url__isnull=False).values('permission__id', 'permission__name', 'permission__title', 'permission__url', 'permission__menu_id', 'permission__parent_id', 'permission__menu__name', 'permission__menu__name', 'permission__menu__icon', 'permission__menu__weight').distinct()
    # 权限字典
    permission_list = {}

    # 菜单字典
    menu_dic = {}
    for i in permission:
        
        permission_list[i['permission__title']] = {
            'id':i['permission__id'],
            'url':i['permission__url'],
            'name':i['permission__name'],
            'title':i['permission__title'],
            'menu_id':i['permission__menu_id'],
            'pid':i['permission__parent_id']
        }

        menu = i['permission__menu_id']

        if menu:
            menu_dic.setdefault(menu, {
                'title': i['permission__menu__name'],
                'icon': i['permission__menu__icon'],
                'weight': i['permission__menu__weight'],
                'children': []
            })
            menu_dic[menu]['children'].append({
                'title': i['permission__name'],
                'url': i['permission__url'],
                'id': i['permission__id'],
            })

    request.session['is_login'] = True
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    request.session[settings.MENU_SESSION_KEY] = menu_dic