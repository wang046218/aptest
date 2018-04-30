# coding:utf-8

"""
rbac API测试

用于服务线上测试

仅仅演示功能/删除了绝大部分配置

API_PR_DETIAL = '/api/blog/' 查看所有文章,新建文章
API_PR_ALL = '/api/blogs/' 查看，局部修改，删除文章

简单起见,文章仅title可编辑

1. 数据库初始化时，默认新建3个用户,['admin', 'random1', 'random2'],一个管理员两个普通用户
2. 关于登录,只需在请求COOKIES中增加 'username':'admin' 一组值即可，实现伪登录
3. 所有url必须以slash结尾,否则报权限错误
4. 错误/异常: 返回键值对 {'Fail': 'reason'} json数据

-----------------------
/api/blogs/

GET {
    'nums': nums_of_blogs,
    'blogs': {
        title_of_blog1: id_of_blog1,
        .......
        }
}

POST 在data数据中传入 { 'title': new_title } 缺省值：Default
return {
    title_of_new_blog: id_of_new_blog
} 表示新建对象的title和id
------------------------


---------------------------
/api/blog/<blog_id>/

Exception 对象不存在

{
    'Fail': reason
}

GET {
id : title
}

PUT # 支持修改文章blog.title属性
# 表单数据中 title = newtitle
返回{
    id: new_title
}


DETELE { # 返回被删除文章的id/title
    "blog": [
        7 #删除的blog id
    ],
    "access": [
        "/api/blog/7/" # 删除的网址
    ],
    "roleacess": [
        15, #删除的roleaccess记录的id
        16
    ]
}


------------------
6张数据表
- Blog
- User
- UserRole
- Role
- RoleAccess
- Access

"""

from __future__ import unicode_literals

from django.test import TestCase, Client

import unittest

from role.models import Role, User, Access, RoleAccess, Blog, UserRole

HOST = 'http://127.0.0.1:8000'
USERNAME = ['admin', 'random1', 'random2']


class MyClient(Client):
    """定制一下Client, 代入特定参数"""
    def get(self, path, user='admin', data=None, follow=False, secure=False, **extra):
        self.cookies['username'] = user
        return super(MyClient, self).get(path, data, follow, secure, **extra)

    def post(self, path, user='admin', data=None):
        self.cookies['username'] = user
        data = {'title': 'new post'}
        return super(MyClient, self).post(path, data)

    def patch(self, path, user='admin', title=None, data=None):
        self.cookies['username'] = user
        if title:
            self.cookies['title'] = title
        return super(MyClient, self).patch(path)

    def delete(self, path, user='wzj', data=None):
        self.cookies['username'] = user
        return super(MyClient, self).delete(path)


class MyApiTest(TestCase):

    def setUp(self):
        self.client = MyClient()
        create_data()  # 初始化数据
        return None

    def test_get(self):
        # 1 /api/blogs/ GET 查看所有人的文章
        res1 = self.client.get('/api/blogs/', user='random1').json()
        res2 = self.client.get('/api/blogs/', user='random2').json()
        res = self.client.get('/api/blogs/', user='admin').json()
        self.assertEqual(res1['nums'], res2['nums'])
        self.assertEqual(res1['nums'], res['nums'])

    def test_blog_post(self):
        nums_of_blog = Blog.objects.count()
        nums_of_Acc = RoleAccess.objects.count()
        self.client.post('/api/blogs/', user='random1', data={'title': 'new title_of_'})
        self.client.post('/api/blogs/', user='random2', data={'title': 'new title_of_'})
        self.client.post('/api/blogs/', user='admin', data={'title': 'new title_of_'})
        new_unms_blog = Blog.objects.count()
        new_nums_acc = RoleAccess.objects.count()
        self.assertEqual(nums_of_blog+3, new_unms_blog)
        self.assertEqual(nums_of_Acc+6, new_nums_acc)

    def test_get_blog(self):
        for blog in Blog.objects.all():
            for user in USERNAME:
                res = self.client.get('/api/blog/'+str(blog.id)+'/', user=user)
                self.assertEqual(res.status_code, 200)

    def test_patch(self):
        pass

    def test_delete(self):
        pass


def create_data():
    # create Role
    admin_id = Role.objects.create(name='admin').id
    other_id = Role.objects.create(name='other').id
    # create User
    user_wzj_id = User.objects.create(name='admin', is_admin=1).id
    user_random_1_id = User.objects.create(name='random1').id
    user_random_2_id = User.objects.create(name='random2').id
    # 每个人的角色是单一的
    # create Blog
    blog_data = [
        ['tile2', user_random_1_id],
        ['tile3', user_random_1_id],
        ['tile4', user_random_2_id],
        ['tile5', user_random_2_id],
    ]
    blog_url = []
    for blog in blog_data:
        b_id = Blog.objects.create(title=blog[0], author_id=blog[1]).id
        blog_url.append(('/api/blog/%d/' % b_id, blog[1]))
    # create UserRole
    UserRole.objects.create(uid=user_wzj_id, role_id=admin_id)
    UserRole.objects.create(uid=user_random_1_id, role_id=other_id)
    UserRole.objects.create(uid=user_random_2_id, role_id=other_id)

    # create Access
    urls = blog_url  # 详情页
    for url, blog_id in urls:
        acc_id = Access.objects.create(urls=url).id
        RoleAccess.objects.create(role_id=admin_id, access_id=acc_id)
        RoleAccess.objects.create(role_id=other_id, access_id=acc_id)

    url = '/api/blogs/'
    acc_id = Access.objects.create(urls=url).id
    RoleAccess.objects.create(role_id=admin_id, access_id=acc_id)
    RoleAccess.objects.create(role_id=other_id, access_id=acc_id)


if __name__ == '__main__':
    unittest.main()
