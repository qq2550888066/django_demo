from django.conf.urls import url

from book import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # url(r'book/$', views.BooksAPIView1.as_view()),
    # url(r'book/(?P<pk>\d+)$', views.BooksAPIView2.as_view()),
]
# 可以处理视图的路由器
router = DefaultRouter()
# 注册
router.register(r'books', views.BookInfoViewSet)
# 添加
urlpatterns += router.urls
