from django.conf.urls import url

#  urlpatterns 是被Django自动识别的路由变量
from users import views

urlpatterns = [
    # 每一个路由变量都需要被 url  函数来构造
    # url(路径, 视图)
    url(r'^index/$', views.index,name='index'),
    url(r'^say/$', views.say),
]
