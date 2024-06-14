## 权限组件的使用

1. 先把rbac 的app拷贝到新项目中，并且注册

   ```python
   INSTALLED_APPS = [
   	...
       'rbac.apps.RbacConfig'
   ]
   ```

2. 数据库的迁移

   如果是使用其他项目的用户表

   修改rbac的用户表

   ```python
   class User(models.Model):
       # username = models.CharField(max_length=32, verbose_name="用户名")
       # password = models.CharField(max_length=32, verbose_name="密码")
       roles = models.ManyToManyField(Role, blank=True)
   
       def __str__(self):
           return self.username
   
       class Meta:
           verbose_name = "用户表"
           verbose_name_plural = verbose_name
           abstract = True   # 数据库迁移时 不会生成表  当做基类
   ```

   其他项目的用户表继承rbac的用户表

   ```python
   from rbac.models import User
   
   class UserProfile(User):
   ```

   删除rbac中migrations的迁移记录

   执行数据库迁移的命令

   ```python 
   python manage.py makemigrations
   python manage.py  migrate
   ```

3. 配置rbac的路由

   ```python 
   urlpatterns = [
     	...
       url(r'^rbac/', include('rbac.urls', namespace='rbac')),
   ]
   
   ```

4. 录入权限信息

   /rbac/role/list/    角色管理

   /rbac/menu/list/    菜单管理

   /rbac/multi/permissions/   批量操作权限

5. 分配权限

   分配权限前指定User

   /rbac/distribute/permissions/

6. 注册中间件 + 在settings中配置

   ```python
   # 白名单
   WHITE_LIST = [
       r'^/login/$',
       r'^/register/$',
       r'^/admin/',
   ]
   
   # 免认证的地址
   PASS_LIST = [
       r'^/index/$'
   ]
   
   # 权限的session key
   PERMISSION_SESSION_KEY = 'permission'
   # 菜单的session key
   MENU_SESSION_KEY = 'menu'
   
   ```

7. 登录成功后进行权限信息的初始化

   ```python
   from rbac.service.permission_init import permission_init
   
   permission_init(request, user_obj)
   
   ```

8. 使用二级菜单

   在母版中修改

   ```
    {% load rbac %}
    {% menu2 request %}
   ```

   导入css和js

   ```
   <link rel="stylesheet" href="{% static 'rbac/css/menu.css' %}">
   <script src="{% static 'rbac/js/menu.js' %} "></script>
   ```

9. 路径导航

   ```
   {% breadcrumb request %}
   ```

10. 权限控制到按钮级别

    ```
     {% if request|has_permission:'class_add' %}
    
    <a class="btn btn-primary btn-sm" href="{% reverse_url request 'class_add' %}">新增</a>
     {% endif %}
    ```

    
