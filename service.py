from django.conf import settings


def service(request, obj):
    permission = obj.role.filter(permission__url__isnull=False).values('permission__name', 'permission__url', 'permission__menu', 'permission__menu__name', 'permission__menu__icon', 'permission__menu__weight').distinct() 

    permission_list = []

    # 菜单字典

    menu_dict = {}

    for i in permission:
        permission_list.append('permission__url')
        menu = i['permission__menu']
        if menu:
            menu_dict.setdefault(menu, {
                'title': i['permission__menu__name'],
                'icon': i['permission__menu__icon'],
                'weight': i['permission__menu__weight'],
                'children': []
            })
            menu_dict[menu]['children'].append({
                'title': i['permission__name'],
                'url': i['permission__url']
            })
    request.session['is_login'] = True
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list
    request.session[settings.MENU_SESSION_KEY] = menu_dict