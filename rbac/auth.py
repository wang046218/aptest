# coding: utf-8
from __future__ import unicode_literals

from django.utils.deprecation import MiddlewareMixin

from django.http import JsonResponse, HttpResponse
from role.models import User, UserRole, Access, RoleAccess


class AuthMiddleware(MiddlewareMixin):

    def get_perm(self, request):
        """查看是否有访问URL的权限"""
        result = False
        urls = request.path
        # 未登录
        if 'username' not in request.COOKIES.keys():
            return JsonResponse({'Fail': 'COOKIES missing key:username'}, status=401)

        username = request.COOKIES['username']
        #  检查用户名是否合法
        try:
            uid = User.objects.get(name=username).id
        except User.DoesNotExist:
            return JsonResponse({'Fail': 'username:%s unregister' % username}, status=401)

        try:  # 检查用户是否赋予用户组
            user_role = UserRole.objects.get(uid=uid)
        except UserRole.DoesNotExist:
            return JsonResponse({'Fail': 'missing role message'}, status=409)

        rid = user_role.role_id

        # 查询角色所有访问权限的url Access记录
        perm_acc = RoleAccess.objects.filter(role_id=rid)

        if perm_acc:
            access_id = [access.access_id for access in perm_acc]
            # 查找所访问的url是否在权限列表中
            acc_info = Access.objects.filter(id__in=access_id).filter(urls=urls)
            if acc_info:
                result = True
        return result

    def process_request(self, request):
        if not request.path.startswith('/api/blog'):
            # 对path进行简单判断
            return JsonResponse({'Fail': 'unknown path'}, status=404)
        res = self.get_perm(request)
        if isinstance(res, HttpResponse):
            return res
        if not res:
            return JsonResponse({'Fail': 'perm deny'}, status=401)
        return
