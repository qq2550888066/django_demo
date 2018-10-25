from django.conf.urls import url

from users.views import *

urlpatterns = [
    url(r'^index/$', index),  # 不可以使用函数调用 url(r'index',index())
    url(r'^index1$', index1, name='index1'),
    url(r'^index2$', index2, name='index2'),

    # 获取请求数据
    # 解析URL
    url(r'^weather/(\w+)/(\d+)$', weather),
    # 分组命名
    url(r'^weather_named/(?P<city>\w+)/(?P<year>\d+)$', weather_named),

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

    # 构建响应对象
    url(r'^create_response$', create_response),

    # 构建json响应
    url(r'^create_json$', create_json),

    # 重定向
    url(r'^redirect_response$', redirect_response),

    # 设置cookie
    url(r'^set_cookie$', set_cookie),
    # 读取cookie
    url(r'^read_cookie$', read_cookie),

    # 设置session
    url(r'^set_session$', set_session),
    # 读取session
    url(r'^read_session$', read_session),

    # 绑定类视图
    # url(r'^demo_view$', my_decorator(DemoView.as_view()))
    url(r'^demo_view$', DemoView.as_view()),

    # 模板渲染
    url(r'^render_template$', render_template)
]

# r'index'
# index1 ,index2,index234523512
# users/index1
#
