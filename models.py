from django.db import models

# Create your models here.

class Menu(models.Model):
    name = models.CharField('名称', max_length=32)
    icon = models.CharField('图标', max_length=32)
    weight = models.IntegerField('权重')
    class Meta:
        verbose_name = '菜单表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField('名称', max_length=32)
    title = models.CharField('别名', max_length=32)
    url = models.CharField('URL', max_length=32)
    menu = models.ForeignKey('Menu', verbose_name='所属菜单', blank=True, null=True)
    parent = models.ForeignKey('Permission', verbose_name='父级菜单', blank=True, null=True)
    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField('角色名称', max_length=32)
    permission = models.ManyToManyField('Permission', '权限')
    class Meta:
        verbose_name = '角色表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    role = models.ManyToManyField('Role')
    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username