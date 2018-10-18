import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from datetime import datetime

from django.views import View
from rest_framework.viewsets import ModelViewSet

from book.models import BookInfo
from book.serializers import BookInfoSerializer1


class BooksAPIView1(View):
    """
    查询所有图书、增加图书
    """

    def get(self, request):
        """
        查询所有图书
        路由：GET /books/
        """
        queryset = BookInfo.objects.all()
        book_list = []
        for book in queryset:
            book_list.append({
                'id': book.id,
                'btitle': book.btitle,
                'bpub_date': book.bpub_date,
                'bread': book.bread,
                'bcomment': book.bcomment,
                'image': book.image.url if book.image else ''
            })
        return JsonResponse(book_list, safe=False)

    def post(self, request):
        """
        添加图书
        :param request:
        :return:
        """
        # 获取图书数据
        book_byte = request.body
        book_str = book_byte.decode()
        data = json.loads(book_str)

        # 校验数据
        if data.get("btitle", "") == "":
            return JsonResponse({"error": "必须提供标题"}, status=403)

        # 创建图书模型
        book = BookInfo()
        book.btitle = data.get("btitle")
        book.bpub_date = datetime.strptime(data.get('bpub_date'), '%Y-%m-%d')
        book.save()

        # 将新的模型返回
        return JsonResponse({
            "id": book.id,
            "btitle": book.btitle,
            "bcomment": book.bcomment,
            "bpub_date": book.bpub_date,
            "bread": book.bread,
            "image": book.image.url if book.image else "",
        }, status=201)


class BooksAPIView2(View):
    def get(self, request, pk):
        """
        获取单个图书数据
        :param request:
        :param pk:
        :return:
        """
        # 获取校验数据
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        # 返回json数据
        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'image': book.image.url if book.image else ''
        })

    def put(self, request, pk):
        """
        修改单个图书数据
        :param request:
        :param pk:
        :return:
        """
        # 获取校验数据
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        # 获取图书数据
        book_byte = request.body
        book_str = book_byte.decode()
        data = json.loads(book_str)
        # 校验数据
        if data.get("btitle", "") == "":
            return JsonResponse({"error": "必须提供标题"}, status=403)

        # 修改数据
        # 创建图书模型
        book.btitle = data.get("btitle")
        book.bpub_date = datetime.strptime(data.get('bpub_date'), '%Y-%m-%d')
        book.save()

        # 返回json数据
        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'image': book.image.url if book.image else ''
        })

    def delete(self, request, pk):
        """
        删除单个图书数据
        :param request:
        :return:
        """
        # 获取校验数据
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        book.delete()

        return HttpResponse("删除成功", status=204)

class BookInfoViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer1


