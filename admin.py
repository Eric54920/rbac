from django.contrib import admin
from .models import Menu, Permission, Role, User
# Register your models here.

class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'icon', 'weight']
    list_editable = ['name', 'icon', 'weight']

admin.site.register(Menu, MenuAdmin)

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'title', 'url', 'menu', 'parent']
    list_editable = ['name', 'title', 'url', 'menu', 'parent']
admin.site.register(Permission, PermissionAdmin)

class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name']

admin.site.register(Role, RoleAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password']
    list_editable = ['username', 'password']

admin.site.register(User, UserAdmin)