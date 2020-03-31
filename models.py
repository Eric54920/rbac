from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=32)
    icon = models.CharField(max_length=32)
    weight = models.IntegerField(default=1)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '菜单表'
        verbose_name_plural = verbose_name

class Permission(models.Model):
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=32)
    menu = models.ForeignKey('Menu', blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name

class Role(models.Model):
    name = models.CharField(max_length=32)
    permission = models.ManyToManyField('Permission', blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '角色表'
        verbose_name_plural = verbose_name

class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    role = models.ManyToManyField('Role')
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

