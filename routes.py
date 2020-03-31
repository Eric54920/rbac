from django.conf import settings
from django.utils.module_loading import import_string
from django.urls import RegexURLResolver, RegexURLPattern
from collections import OrderedDict


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """
    None  '/'
     [
        url(r'^', include('web.urls')),
        #  url(r'^rbac/', include('rbac.urls',namespace='rbac')),
    ]



    """

    """
     None  '/^'   
     [
        
            url(r'^login/$', account.login, name='login'),
            url(r'^index/$', account.index, name='index'),
        
            url(r'^customer/list/$', customer.customer_list, name='customer_list'),
            url(r'^customer/add/$', customer.customer_add,name='customer_add'),
            url(r'^customer/edit/(?P<cid>\d+)/$', customer.customer_edit,name='customer_edit'),
            url(r'^customer/del/(?P<cid>\d+)/$', customer.customer_del,name='customer_del'),
        
            url(r'^payment/list/$', payment.payment_list,name='payment_list'),
            url(r'^payment/add/$', payment.payment_add,name='payment_add'),
            url(r'^payment/edit/(?P<pid>\d+)/$', payment.payment_edit,name='payment_edit'),
            url(r'^payment/del/(?P<pid>\d+)/$', payment.payment_del,name='payment_del'),
        ]
    
    """

    for item in urlpatterns:
        if isinstance(item, RegexURLResolver):
            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace,)
                else:
                    namespace = pre_namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            #  None  '/^'
            recursion_urls(namespace, pre_url + item.regex.pattern, item.url_patterns, url_ordered_dict)
        else:

            if pre_namespace:
                name = "%s:%s" % (pre_namespace, item.name,)
            else:
                name = item.name
            if not item.name:
                raise Exception('URL路由中必须设置name属性')
            #  '/^^login/$'   '/login/'
            url = pre_url + item._regex
            url_ordered_dict[name] = {'name': name, 'url': url.replace('^', '').replace('$', '')}


def get_all_url_dict(ignore_namespace_list=None):
    """
    获取路由中
    :return:
    """
    ignore_list = ignore_namespace_list or []
    url_ordered_dict = OrderedDict()

    md = import_string(settings.ROOT_URLCONF)  # 'luffy_permission.urls'
    urlpatterns = []

    """
     [
        url(r'^admin/', admin.site.urls),
        url(r'^', include('web.urls')),
        #  url(r'^rbac/', include('rbac.urls',namespace='rbac')),
    ]
    视图                  RegexURLPattern
    路由分发 include      RegexURLResolver

    """

    for item in md.urlpatterns:
        if isinstance(item, RegexURLResolver) and item.namespace in ignore_list:
            continue
        urlpatterns.append(item)
    recursion_urls(None, "/", urlpatterns, url_ordered_dict)
    return url_ordered_dict
