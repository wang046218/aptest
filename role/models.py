# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Blog(models.Model):

    title = models.CharField(max_length=50)
    author_id = models.IntegerField(default=0)
    content = models.CharField(max_length=550, default='default')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class User(models.Model):
    name = models.CharField(max_length=20, default='')
    email = models.CharField(max_length=30, default='')
    # 是否管理员 0->非管理员     1->管理员
    is_admin = models.SmallIntegerField(default=0)
    status = models.SmallIntegerField(default=1)
    updated_time = models.DateTimeField(auto_now_add=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "用户->%s" % self.name


class Role(models.Model):
    name = models.CharField(max_length=20, default='')
    status = models.SmallIntegerField(default=1)
    updated_time = models.DateTimeField(auto_now_add=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Role:%s" % self.name


class UserRole(models.Model):
    uid = models.IntegerField()
    role_id = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)


class Access(models.Model):
    # 权限名称
    title = models.CharField(max_length=50, default='')
    urls = models.CharField(max_length=1000, default='')
    # 状态 0->无效, 1->有效
    status = models.SmallIntegerField(default=1)
    updated_time = models.DateTimeField(auto_now_add=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.urls


class RoleAccess(models.Model):
    role_id = models.IntegerField()
    access_id = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "r_id:->%s" % self.role_id
