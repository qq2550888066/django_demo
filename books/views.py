from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import *
from rest_framework.viewsets import ViewSet, GenericViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.exceptions import APIException
from django.db import DatabaseError

from books.models import BookInfo
from books import serializers


class DemoApiView(APIView):

    # 返回书籍列表数据
    def get(self, request):
        # request Request对象
        print(request)
        # 1. 查询所有书籍
        # 2. 构建序列化对象
        # 3. 返回response
        books = BookInfo.objects.all()
        bses = serializers.ModelsSerializerBookInfo(books, many=True)
        return Response(data=bses.data)


class DemoApiView2(ListAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = serializers.ModelsSerializerBookInfo

    # 不用用户能看到的字段是不同的
    def get_serializer_class(self):
        # 判断用户类型
        # 如果是超级管理员 返回serializers.ModelsSerializerBookInfo
        # 如果是普通用户 返回serializers.ModelsNormalSerializerBookInfo
        user = self.request.user
        if user.is_superuser:
            return serializers.ModelsSerializerBookInfo
        else:
            return serializers.ModelsNormalSerializerBookInfo

    # 需要根据用户类型来返回不同的数据
    def get_queryset(self):
        # 判断用户类型
        # 如果是超级管理员 返回所有数据
        # 如果是普通用户   返回未被删除的数据
        user = self.request.user
        if user.is_superuser:
            return BookInfo.objects.all()
        else:
            return BookInfo.objects.filter(is_delete=False)

    # def get(self, request):
    #     return  self.list(request)
    # books = self.get_queryset()
    # bses = self.get_serializer(books, many=True)
    # return Response(data=bses.data)


class BookApiView(ViewSet):
    # 获取所有图书 GET    /books   list     get-->list
    # 创建图书    POST   /books   create   post-->create
    # 获取单个图书 GET    /books/<pk>  retrieve get--> retrieve
    # 更新单个图书 PUT    /books/<pk> update    put--> update
    # 删除单个图书 DELETE /books/<pk>  destroy  delete-->destroy

    # books {'get':"list","post":'create'}
    # books/<pk>  {'get':'retrieve','put':'update','delete':'destroy'}
    def list(self, request):
        return Response('list')

    def create(self, request):
        return Response('create')

    def retrieve(self, request, pk):
        return Response('retrieve')

    def update(self, request, pk):
        return Response('update')

    def destroy(self, request, pk):
        return Response('destroy')


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return False


class CustomPagnation(PageNumberPagination):
    page_size = 2
    max_page_size = 5
    page_size_query_param = 'page_size'


class CustomLimit(LimitOffsetPagination):
    default_limit = 4
    limit_query_param = 'limit'
    max_limit = 7


class BookGenericApiView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    get:
    查询数据

    list:
    查询数据

    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (CustomPermission,)
    throttle_scope = 'books'
    # filter_fields = ['bread', 'id']
    filter_backends = [OrderingFilter]
    ordering_fields = ['id', 'bpub_date']
    queryset = BookInfo.objects.all()
    serializer_class = serializers.ModelsSerializerBookInfo

    pagination_class = CustomLimit

    # 获取所有图书 GET    /books   list     get-->list
    # 创建图书    POST   /books   create   post-->create
    # 获取单个图书 GET    /books/<pk>  retrieve get--> retrieve
    # 更新单个图书 PUT    /books/<pk> update    put--> update
    # 删除单个图书 DELETE /books/<pk>  destroy  delete-->destroy

    # books {'get':"list","post":'create'}
    # books/<pk>  {'get':'retrieve','put':'update','delete':'destroy'}
    # def list(self, request):
    #     return Response('list')

    # 不用用户能看到的字段是不同的
    # def get_serializer_class(self):
    #     # 判断用户类型
    #     # 如果是超级管理员 返回serializers.ModelsSerializerBookInfo
    #     # 如果是普通用户 返回serializers.ModelsNormalSerializerBookInfo
    #     action = self.action
    #     # 如果action=='list'
    #     # 如果action!='list'
    #     user = self.request.user
    #     if user.is_superuser:
    #         return serializers.ModelsSerializerBookInfo
    #     else:
    #         return serializers.ModelsNormalSerializerBookInfo

    # 需要根据用户类型来返回不同的数据
    def get_queryset(self):
        # 判断用户类型
        # 如果是超级管理员 返回所有数据
        # 如果是普通用户   返回未被删除的数据
        action = self.action
        user = self.request.user
        if user.is_superuser:
            return BookInfo.objects.all()
        else:
            return BookInfo.objects.filter(is_delete=False)

    def create(self, request):
        return Response('create')

    # def retrieve(self, request, pk):
    #     return Response('retrieve')

    def update(self, request, pk):
        return Response('update')

    def destroy(self, request, pk):
        return Response('destroy')

    # 获取最后一本书
    @action(methods=['get'], detail=False)  # books/latest
    def latest(self, request):
        # latest self.action=='latest'
        # 找到最后一本书
        # 序列化输出
        book = BookInfo.objects.latest('id')
        bs = self.get_serializer(book)
        return Response(data=bs.data)

    @action(methods=['get'], detail=True)  # books/<pk>/read
    def read(self, request, pk):
        # self.action == 'read'
        # 获取对象
        # 更新对象
        # 序列化输出
        raise APIException
        # raise DatabaseError

        book = self.get_object()
        book.bread += 1
        book.save()
        bs = self.get_serializer(book)
        return Response(data=bs.data)
