# coding: ut-f

"""

rbac API测试

用于服务线上测试

仅仅演示功能/删除了绝大部分配置

API_PR_DETIAL = '/api/blog/' 查看所有文章,新建文章
API_PR_ALL = '/api/blogs/' 查看，局部修改，删除文章

简单起见,文章仅title可编辑

1. 数据库初始化时，默认新建3个用户,['admin', 'random1', 'random2'],一个管理员两个普通用户
2. 关于登录,只需在请求COOKIES中增加 'username': admin 一组值即可，实现伪登录
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
    title: id
}

PATCH # 支持修改文章blog.title属性,设置cookies {'title': new_title}
返回{
    id: new_title
}


DETELE { # 返回被删除文章的id/title
    title: id
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


import requests
import unittest

HOST = 'http://127.0.0.1:8000'
USERNAME = ['admin', 'random1', 'random2']


class TestAPIError(unittest.TestCase):
    """requests测试异常请求"""
    def setUp(self):
        self.path = '/api/blogs/'
        self.url = HOST + self.path
        self.errror_cookies = {'usererror': 'tstst'}

    # 未登录: COOKIES 未定义username
    def test_login(self):
        res = requests.get(self.url)
        self.assertEqual(res.status_code, 401)  # missing username
        res = requests.get(self.url, cookies=self.errror_cookies)
        self.assertEqual(res.status_code, 401)  # missing username

    def test_404(self):
        """url 错误/请求对象不存在"""
        res = requests.get(HOST+'/error_url/')
        self.assertEqual(res.status_code, 404)
        res = requests.get(HOST + '/api/blog/1000/')



    def get_blog_nums(self, username):
        # /api/blog/   GET 查看所有
        cookies = {'username': username}
        # jres_dict = requests.get(path, cookies=cookies)
        # return res_dict['nums']

    def blog_post(username, blog_title="default"):
        # /api/blog/   POST 发布新文章
        cookies = {'username': username}
        data = {'title': blog_title}
        # res = requests.post(path, cookies=cookies, data=data)
        # return res

if __name__ == '__main__':
    unittest.main()

