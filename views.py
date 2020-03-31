from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseNotFound
from rbac import models
from rbac.forms import RoleForm, MenuForm, PermissionForm, MultiPermissionForm
from django.db.models import Q
from django.forms import modelformset_factory, formset_factory
from rbac.routes import get_all_url_dict

def delete(request, table, pk):
    model = getattr(models, table.title())
    if not table:
        return render(request, 'error.html', {'msg': '所访问的页面不存在'})

    obj = model.objects.filter(pk=pk).first()
    if not obj:
        return render(request, 'error.html', {'msg': '数据不存在'})
    obj.delete()
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)

def role_list(request):
    all_role = models.Role.objects.all()
    return render(request, 'role_list.html', {'all_role': all_role})

def role_change(request, pk=None):
    obj = models.Role.objects.filter(pk=pk).first()
    form_obj = RoleForm(instance=obj)
    if request.method == "POST":
        form_obj = RoleForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:role_list'))
    return render(request, 'form.html', {'form_obj':form_obj})

def menu_list(request):
    mid = request.GET.get('mid')
    if mid:
        permissions = models.Permission.objects.filter(Q(menu_id=mid)|Q(parent__menu_id=mid)).values('pk','name', 'title', 'url', 'menu', 'menu__name', 'parent_id').distinct()
    else:
        permissions = models.Permission.objects.all().values('pk','name', 'title', 'url', 'menu', 'menu__name', 'parent_id').distinct()
    all_menu = models.Menu.objects.all()
    per_lst = {}
    for i in permissions:
        menu = i['menu']
        if menu:
            pk = i['pk']
            per_lst.setdefault(pk, {
                'pk': i['pk'],
                'name': i['name'],
                'url': i['url'],
                'title': i['title'],
                'menu': i['menu'],
                'menu_name': i['menu__name'],
                'sub_menu': []
            })
    for j in permissions:
        if j['parent_id']:
            parent = j['parent_id']
            per_lst[parent]['sub_menu'].append({
                'pk': j['pk'],
                'name': j['name'],
                'url': j['url'],
                'title': j['title'],
                'menu': j['menu'],
                'menu_name': j['menu__name'],
                'parent': j['parent_id']
            })
    return render(request, 'menu_list.html', {'all_menu':all_menu, 'per_lst': per_lst.values()})

def menu_change(request, pk=None):
    obj = models.Menu.objects.filter(pk=pk).first()
    form_obj = MenuForm(instance=obj)
    if request.method == "POST":
        form_obj = MenuForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:menu_list'))
    return render(request, 'menu_form.html', {'form_obj':form_obj})

def permission_change(request, pk=None):
    obj = models.Permission.objects.filter(pk=pk).first()
    form_obj = PermissionForm(instance=obj)
    if request.method == "POST":
        form_obj = PermissionForm(request.POST, instance=obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:menu_list'))
    return render(request, 'form.html', {'form_obj':form_obj})

def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """
    post_type = request.GET.get('type')
    # 编辑和删除的formset
    FormSet = modelformset_factory(models.Permission, MultiPermissionForm, extra=0)
    # 新增的formset
    AddFormSet = formset_factory(MultiPermissionForm, extra=0)
    # 数据库中所有的权限
    permissions = models.Permission.objects.all()
    # 路由系统中所有的权限
    router_dict = get_all_url_dict(ignore_namespace_list=['admin', ])
    # 数据库中权限别名的集合
    permissions_title_set = set([i.title for i in permissions])
    # 路由系统中权限别名的集合
    router_name_set = set(router_dict.keys())

    #  新增的nameset
    add_name_set = router_name_set - permissions_title_set
    add_formset = AddFormSet(initial=[row for name, row in router_dict.items() if name in add_name_set])

    if request.method == 'POST' and post_type == 'add':
        add_formset = AddFormSet(request.POST)
        if add_formset.is_valid():
            permission_obj_list = [models.Permission(**i) for i in add_formset.cleaned_data]
            query_list = models.Permission.objects.bulk_create(permission_obj_list)
            add_formset = AddFormSet()
            for i in query_list:
                permissions_title_set.add(i.title)
    #  删除的nameset
    del_name_set = permissions_title_set - router_name_set
    del_formset = FormSet(queryset=models.Permission.objects.filter(title__in=del_name_set))
    #  更新的nameset
    update_name_set = permissions_title_set & router_name_set
    update_formset = FormSet(queryset=models.Permission.objects.filter(title__in=update_name_set))

    if request.method == 'POST' and post_type == 'update':
        update_formset = FormSet(request.POST)
        if update_formset.is_valid():
            update_formset.save()
            update_formset = FormSet(queryset=models.Permission.objects.filter(title__in=update_name_set))

    return render(
        request,
        'multi_permissions.html',
        {
            'del_formset': del_formset,
            'update_formset': update_formset,
            'add_formset': add_formset,
        }
    )