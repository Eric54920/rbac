from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import redirect, HttpResponse
import re

class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        url = request.path_info
        for i in settings.WHITE_LIST:
            if re.match(r'^{}'.format(i), url):
                return
        if not request.session.get('is_login'):
            return redirect('/login/')

        for i in settings.FREE_AUTH:
            if re.match(r'^{}$'.format(i), url):
                return
        
        for i in request.session.get(settings.PERMISSION_SESSION_KEY):
            if re.match(r'^{}'.format(i), url):
                return
            
        return HttpResponse('没有权限')