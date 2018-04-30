# 简单的博客系统 权限管理

一些说明:

系统基于DJango 1.11 和 Py 2.7.10 搭建

采用Django（runserver）启动即可

开启方法：

- 初始化数据库表,数据库名称为 api2 (mysql 下sql脚本见附件)

- 新建virtualenv, py版本2.7.10,安装依赖包

- 虚拟环境下执行 `python manange.py runsrver` 即可在默认8000端口开启

在虚拟环境下,确定项目路径下manage.py 有 x 权限

注意: 项目中的sql语句在mysql 5.6 下测试通过


IMPORTANT: 项目已经部署在地址 主机159.89.136.76 之上

主机信息

地址: 159.89.136.76




1. 数据库初始化时，默认新建3个用户,['admin', 'random1', 'random2'],一个管理员两个普通用户, 用户组有两个[‘admin', 'other']
2. 关于登录,只需在请求COOKIES中增加 'username':'admin' 一组值即可，实现伪登录
3. 错误/异常: 返回键值对 {'Fail': 'reason'} json数据

## API 接口
path = /api/blogs/

- GET 获取文章列表

测试示例代码

```py
import requests

url = "http://159.89.136.76/api/blogs/"

cookies = {
    'username':'admin'
}

response = requests.get(url, cookies=cookies)
print(response.text)

# 返回 虽然这里表示字典，但实际返回的是json字符串

{
    'nums': nums_of_blogs,
    'blogs': {
        title_of_blog1: id_of_blog1,
        .......
        }
}

```

- POST 新建文章


```py
import requests

url = "http://159.89.136.76/api/blogs/"

cookies = {
    'username':'admin',
}

playload = {
    'title': 'new_title'
}

response = requests.post(url, data=playload, cookies=cookies)
print(response.text)

# 返回

{
    title_of_new_blog: id_of_new_blog
} 表示新建对象的title和id


```
-----------------------------

path = /api/blog/id_blog/

- GET 文章详情

```py
import requests

url = "http://159.89.136.76/api/blog/<id>/"

cookies = {
    'username':'admin'
}

response = requests.get(url, cookies=cookies)
print(response.text)

# 返回
{
    id : title
}
```

- DELETE 删除文章

```py
import requests

url = "http://159.89.136.76/api/blog/<id>/"

cookies = {
    'username':'admin',
}

response = requests.post(url, data=playload, cookies=cookies)

print(response.text)


# 返回

{ # 返回被删除文章的id/title
    "blog": [
        7  #删除的blog id
    ],
    "access": [
        "/api/blog/7/" # 删除对象的地址
    ],
    "roleacess": [
        15, # 删除权限相关记录
        16
    ]
}

```

- patch 修改

支持修改title

```py
import requests

url = "http://159.89.136.76/api/blog/<id>/"

cookies = {
    'username':'admin',
}

playload = {
    title: new_title
}

response = requests.patch(url, data=playload, cookies=cookies)

print(response.text)

# 返回

{
    id: new_title
}

```

## 权限表


用户表              ->用户角色关系表: 用户属于哪些角色
用户角色关系表      ->用户表: 用户属于哪些角色
角色表              ->用户角色关系表: 角色拥有哪些用户
用户角色关系表      ->角色表: 角色拥有哪些用户
角色表              ->角色关系表: 角色拥有哪些操作
角色关系表          ->角色表: 角色拥有哪些操作
角色关系表          ->权限表: 角色拥有哪些权限j
