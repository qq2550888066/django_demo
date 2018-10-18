from django.conf.urls import url

from book import views

urlpatterns = [
    url(r'book/$', views.BooksAPIView1.as_view()),
    url(r'book/(?P<pk>\d+)$', views.BooksAPIView2.as_view()),
]
