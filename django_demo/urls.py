"""django_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls

from users.views import index

urlpatterns = [
    url(r'^admin/', admin.site.urls),  # django默认添加,用于站点管理

    url(r'^docs/', include_docs_urls(title='My API title')),

    #     url(路径,函数)
    #     url(r'index',index),
    # url(路由前缀, include('blog.urls'))
    url(r'^users/', include('users.urls', namespace='users')),

    # 图书的子路由
    # url(r'^api/', include('books.urls')),
    url(r'^', include('books.urls')),
]
