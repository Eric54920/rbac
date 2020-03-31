from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import re
from django.shortcuts import render, redirect, HttpResponse

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        url = request.path_info
        # 是否在白名单中
        for i in settings.WHITE_LIST:
            if re.match(r'^{}'.format(i), url):
                return
        # 是否登录
        if not request.session.get('is_login'):
            return redirect('/login/')
        # 是否免认证
        request.current_menu_id = None
        for i in settings.FREE_AUTH:
            if re.match(r'^{}$'.format(i), url):
                return
        # 是否有权限
        for i in request.session.get(settings.PERMISSION_SESSION_KEY).values():
            # print(i)
            if re.match(r'^{}$'.format(i['url']), url):
                if i['menu_id']:
                    request.current_menu_id = i['id']
                else:
                    request.current_menu_id = i['pid']
                return
        return HttpResponse('没有权限')