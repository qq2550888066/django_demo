from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

# urlpatterns = [
#     # url(r'^books$', views.BooksApiView.as_view()),
#     # url(r'^books/(?P<pk>\d+)$', views.BookApiView.as_view())
# ]
#
# router = DefaultRouter()  # 可以处理视图的路由器
# router.register(r'books', views.BookInfoViewSet)  # 向路由器中注册视图集
#
# urlpatterns += router.urls  # 将路由器中的所以路由信息追到到django的路由列表中



# router = SimpleRouter()
router=DefaultRouter()
router.register('books', views.BookGenericApiView, base_name='book')

urlpatterns = [
    url(r'^test$', views.DemoApiView.as_view()),
    url(r'^test2$', views.DemoApiView2.as_view()),
    # url(r'^books$', views.BookApiView.as_view({'get': 'list', 'post': 'create'})),
    # url(r'^books$', views.BookGenericApiView.as_view({'get': 'list', 'post': 'create'})),
    # url(r'^books/(?P<pk>\d+)$', views.BookApiView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}))    url(r'^books$', views.BookApiView.as_view({'get': 'list', 'post': 'create'})),
    # url(r'^books/(?P<pk>\d+)$',
    #     views.BookGenericApiView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    # url(r'^books/latest$', views.BookGenericApiView.as_view({'get': "latest"})),
    # url(r'^books/(?P<pk>\d+)/read$', views.BookGenericApiView.as_view({'put': "read"}))
    url(r'^',include(router.urls))
]



# urlpatterns += router.urls

# print(urlpatterns)
print(router.urls)
