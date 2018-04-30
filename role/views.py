# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView, View
from django.http import JsonResponse

from django.conf import settings
from django.db import connections

from role.models import User, Access, RoleAccess, Blog, UserRole, Role

class BlogView(ListView):
    """path = /api/blogs/"""
    model = Blog

    def get(self, request, *args, **kwargs):
        self.blogs = self.get_queryset()
        blogs = {blog.id: blog.title for blog in self.blogs}
        num_blog = len(self.blogs)
        out = {'nums': num_blog, 'blogs': blogs}
        return JsonResponse(out, status=200)

    def post(self, request, *args, **kwargs):
        title = self.request.POST.get('title', 'Default')
        user = self.request.COOKIES['username']
        new_blog_id = create_blog(title, user)
        out = {new_blog_id: title}
        return JsonResponse(out, status=200)


class BlogDetailView(View):
    """path = /api/blog/<id>/"""

    def get(self, request, id, *args, **kwargs):
        try:
            blog = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return JsonResponse({'Fail': 'Blog does not Exist'}, status=404)
        out = {
            blog.id: blog.title
        }
        return JsonResponse(out, status=200)

    def patch(self, request, id, *args, **kwargs):
        username = request.COOKIES['username']
        u_id = User.objects.get(name=username).id
        try:
            blog = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return JsonResponse({'Fail': 'Blog does not Exist'}, status=404)
        if blog.author_id != u_id:
            return JsonResponse({'Fail': 'only author can edit'}, status=401)
        else:
            new_title = self.request.POST.get('title')
            if new_title:
                blog.save()
                return JsonResponse({blog.id: blog.title})
            else:
                return JsonResponse({'Fail': 'unchange'}, status=406)

    def delete(self, request, id, *args, **kwargs):
        username = request.COOKIES['username']
        user = User.objects.get(name=username)
        u_id = user.id
        try:
            blog = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            return JsonResponse({'Fail': 'DoesNotExist'})
        if blog.author_id == u_id or user.is_admin:
            # 作者和管理员有权删除文件
            b_id = blog.id
            access_s = Access.objects.filter(urls=settings.API_PR_DETIAL+str(blog.id)+'/')
            blog.delete()
            # 清理url权限
            acc_delete = [access.urls for access in access_s]
            ra_delete = []
            for access in access_s:
                a_id = access.id
                role_access = RoleAccess.objects.filter(access_id=a_id)
                ra_delete = ra_delete + [ro_ss.id for ro_ss in role_access]
                access.delete()
                role_access.delete()
            out = {
                'blog': [b_id],
                'access': acc_delete,
                'roleacess': ra_delete
            }
            return JsonResponse(out)
        return JsonResponse({"Fail": 'perm deny: can‘t delete'})


def create_blog(title, username):
    """新建文章"""
    # 在中间件中已经完成user, role的合法性检查
    user = User.objects.get(name=username)
    user_id = user.id

    b_id = Blog.objects.create(title=title, author_id=user_id).id
    url = settings.API_PR_DETIAL + str(b_id) + '/'

    u_role = UserRole.objects.get(uid=user_id)
    rid = u_role.id

    admin_role_id = Role.objects.get(name='admin').id
    other_role_id = Role.objects.get(name='other').id

    acc_id = Access.objects.create(urls=url).id  # 创建一条权限记录
    RoleAccess.objects.create(role_id=rid, access_id=acc_id)  # 绑定到当前用户组
    if not user.is_admin:  # 绑定到管理员用户组
        RoleAccess.objects.create(role_id=admin_role_id, access_id=acc_id)
    else:
        RoleAccess.objects.create(role_id=other_role_id, access_id=acc_id)
    return b_id
