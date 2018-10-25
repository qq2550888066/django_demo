import json
from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.viewsets import ModelViewSet

from rest_framework import status

from rest_framework.views import APIView

# from books.serializers import BookInfoSerializer
from .models import BookInfo, HeroInfo

from . import serializers


# Create your views here.

# /users/create
# /users/update
# /users/delete
# /user/login

# /user_login
# /create_user
# /update_user

# /users?action=create,update,delete&id=1
# ?btitle=天龙八部&bread=10
# '{"name":"zhangsan","age":10}'
#
# '''
# <root>
# <name>zhangsan</name>
# <age>10</age>
# </root>
# '''

# 获取所有图书 GET    /books
# 创建图书    POST   /books
# 获取单个图书 GET    /books/<pk>
# 更新单个图书 PUT    /books/<pk>
# 删除单个图书 DELETE /books/<pk>

# 获取所有英雄 GET    /heros
# 创建英雄    POST   /heros
# 获取单个英雄 GET    /heros/<pk>
# 更新单个英雄 PUT    /heros/<pk>
# 删除单个英雄 DELETE /heros/<pk>

# def get_data_list(model):
#     objs = model.objects.all()
#     data_list = []
#     for obj in objs:
#         obj_dict = {
#             field: getattr(obj, field, '')
#             for field in [field.name for field in model._meta.fields]
#         }
#         data_list.append(obj_dict)
#     return data_list

def get_data_list(model, serializer_class):
    objs = model.objects.all()
    return serializer_class(objs, many=True).data


class BooksApiView(View):
    model = HeroInfo
    serializer_class = serializers.BookInfoSerializerFull

    # HeroInfo._meta.fields
    # model_fields = [
    #     'id',
    #     'hname',
    #     'hgender',
    #     'hcomment',
    #     'hbook',
    #     'is_delete',
    # ]

    # model = BookInfo
    # model_fields = [
    #     "id",
    #     "btitle",
    #     "bpub_date",
    #     "bread",
    #     "bcomment",
    #     "image",
    # ]

    def get(self, request):
        """
        获取所有图书
        :param request:
        :return:
        """
        # 1. 查询所有图书
        # 2. 构建json数据列表
        # 3. 返回json数据
        # objs=self.model.objects.all()
        # objs = self.model.objects.all()
        # data_list = []
        # for obj in objs:
        #     obj_dict = {
        #         field: getattr(obj, field, '')
        #         for field in [field.name for field in self.model._meta.fields]
        #     }
        #     data_list.append(obj_dict)

        objs = self.model.objects.all()
        data = self.serializer_class(objs, many=True).data
        # 判断客户端接受的数据格式
        return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
        # return render(request, 'index.html', context=data)

    def post(self, request):
        """
        增加图书
        :param request:
        :return:
        """
        # 1. 获取json数据 原始数据-->转换-->python字典
        # 2. 校验数据
        # 3. 创建图书对象
        # 4. 返回新建图书对象

        # 判断客户端请求数据类型
        # json-->json.loads
        # 表单-->request.POST
        # xml-->xml解析器
        # body_raw = request.body
        # body_str = body_raw.decode()
        # data = json.loads(body_str)
        # 如果使用DRF帮助自动解析客户端的数据
        # 那么DRF会解析出来的数据字典保存到Request对象的data属性

        data = request.data

        # 书籍
        # 普通管理员
        # data={
        #     "btitle":"我",# 书名不能超过128个字符,不能少于1个字符
        #     "bread":10,
        #     "bcomment":20,# 阅读量不允许小于评论量
        # }
        # 超级管理
        # data={
        #     "btitle":"我",# 书名不能超过128个字符,不能少于1个字符
        #     "bread":10,
        #     "bcomment":20,# 阅读量不允许小于评论量
        #     "bpub_date":"2018-10-10",
        #     'is_delete':True,# 验证is_delete是否为True
        # }
        # 英雄
        # 普通管理员
        # data={
        #     "hname":"我",# 书名不能超过4个字符,不能少于2个字符
        #     "hgender":10,
        #     "hcomment":20,# 阅读量不允许小于评论量
        # }
        # 超级管理
        # data={
        #     "hname":"我",# 书名不能超过4个字符,不能少于2个字符
        #     "hgender":10,
        #     "hcomment":20,# 阅读量不允许小于评论量
        #     'is_delete':True,# 验证is_delete是否为True
        #     'hbook':1
        # }

        # 数据校验
        bs = serializers.BookInfoSerializerCreate(data=data)
        valid = bs.is_valid()
        if valid:
            # validated_data = bs.validated_data
            # # 保存对象
            # obj = BookInfo.objects.create(**validated_data)
            # obj = bs.create(bs.validated_data)
            obj = bs.save()
        else:
            return JsonResponse(bs.errors, status=400)
        # 序列化输出
        return JsonResponse(serializers.BookInfoSerializerFull(obj).data, status=201)

        # # 校验数据
        # if data.get('btitle', '') == '':
        #     return JsonResponse({"error": "必须提供标题"}, status=400)
        # book = BookInfo()
        # book.btitle = data.get('btitle')
        # book.bpub_date = datetime.strptime(data.get('bpub_date'), '%Y-%m-%d')  # 2018-10-10
        # book.save()

        # book_dict = {
        #     "id": book.id,
        #     "btitle": book.btitle,
        #     "bpub_date": book.bpub_date,
        #     "bread": book.bread,
        #     "bcomment": book.bcomment,
        #     "image": book.image.url if book.image else ''
        # }

        # return JsonResponse(serializers.BookInfoSerializerFull(obj).data, status=201)


def get_data(model, pk):
    try:
        obj = model.objects.get(pk=pk)
    except Exception:
        return JsonResponse({"error": "数据不存在"}, status=404)
    obj_dict = {
        field: getattr(obj, field, '')
        for field in [field.name for field in model._meta.fields]
    }
    return obj_dict


class BookApiView(View):
    model = BookInfo

    def get(self, request, pk):
        """
        获取单个图书
        :param request:
        :param pk:
        :return:
        """
        # 1. 判断对象是否存在
        # 2. 构建json返回
        return JsonResponse(get_data(self.model, pk))

    def put(self, request, pk):
        """
        更新图书
        :param request:
        :param pk:
        :return:
        """
        # 1. 获取json数据
        # 2. 判断对象是否存在
        # 3. 校验数据
        # 4. 更新对象
        # 5. 返回json数据

        body_raw = request.body
        body_str = body_raw.decode()
        data = json.loads(body_str)

        try:
            obj = BookInfo.objects.get(pk=pk)
        except Exception:
            return JsonResponse({"error": "数据不存在"}, status=404)

        bs = serializers.BookInfoSerializerCreate(data=data)
        valid = bs.is_valid()
        if valid:
            # validated_data = bs.validated_data
            # 保存对象
            # for key, value in validated_data.items():
            #     setattr(obj, key, value)
            # obj.save()
            # obj=bs.update(obj, bs.validated_data)
            obj = bs.save()
        else:

            return JsonResponse(bs.errors, status=400)
        # 序列化输出
        return JsonResponse(serializers.BookInfoSerializerFull(obj).data, status=201)

        #
        # # 校验数据
        # if data.get('btitle', '') == '':
        #     return JsonResponse({"error": "必须提供标题"}, status=400)
        #
        # try:
        #     book = BookInfo.objects.get(pk=pk)
        # except Exception:
        #     return JsonResponse({"error": "数据不存在"}, status=404)
        #
        # book.btitle = data.get('btitle')
        # book.save()
        #
        # book_dict = {
        #     "id": book.id,
        #     "btitle": book.btitle,
        #     "bpub_date": book.bpub_date,
        #     "bread": book.bread,
        #     "bcomment": book.bcomment,
        #     "image": book.image.url if book.image else ''
        # }
        #
        # return JsonResponse(book_dict, status=201)

    def delete(self, request, pk):
        """
        删除图书
        :param request:
        :param pk:
        :return:
        """
        # 1. 判断是否存在
        # 2. 删除对象
        # 3. 返回204
        try:
            book = BookInfo.objects.get(pk=pk)
        except Exception:
            return JsonResponse({"error": "数据不存在"}, status=404)

        book.delete()
        return HttpResponse(status=204)


class BookInfoViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer
