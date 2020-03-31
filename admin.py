from django.contrib import admin
from .models import Menu, Permission, Role, User

class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'icon', 'weight']
    list_editable = ['icon', 'weight']

admin.site.register(Menu, MenuAdmin)

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url', 'menu']
    list_editable = ['url', 'menu']

admin.site.register(Permission, PermissionAdmin)

class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name']

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password']
    list_editable = ['username', 'password']

admin.site.register(Role, RoleAdmin)
admin.site.register(User, UserAdmin)


