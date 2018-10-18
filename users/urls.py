from django.conf.urls import url

#  urlpatterns 是被Django自动识别的路由变量
from users.views import *

urlpatterns = [
    # 每一个路由变量都需要被 url  函数来构造
    # url(路径, 视图)
    url(r'^index/$', index, name='index'),
    url(r'^say/$', say),
    # 重定向
    url(r'^response_view/$', response_view),

    url(r'^weather1/([a-z]+)/(\d{4})/$', weather1),
    url(r'^weather2/(?P<city>[a-z]+)/(?P<year>\d{4})/$', weather2),

    # 从查询字符串获取数据
    url(r'^query_params$', query_params),

    # 从请求体获取数据 表单形式
    url(r'^form$', form),
    # 从请求体获取数据 表单形式
    url(r'^json_data$', json_data),

    # 从请求头获取数据
    url(r'^header$', header),

    # 请求对象的其他属性
    url(r'^other$', other),
]
