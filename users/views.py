from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
# from django.urls import reverse
from django.core.urlresolvers import reverse


def index(request):
    """
    创建视图
    :param request:
    :return:
    """
    return HttpResponse("hello world")


def say(request):
    url = reverse("users:index")
    print(url)
    # 跳转到/users/index
    # return redirect(url)
    return HttpResponse("SAY")


# 请求的几种方式
# 1. 按照url路径参数传递
# 未命名参数按定义顺序传递
def weather1(request, city, year):
    print('city=%s' % city)
    print('year=%s' % year)
    return HttpResponse('OK')


# 命名参数按名字传递
def weather2(request, year, city):
    print('city=%s' % city)
    print('year=%s' % year)
    return HttpResponse('OK')


# 获取查询字符串数据
def query_params(request):
    # request.GET 包含查询字符串数据
    data = request.GET
    print(data)
    # 打印单个值
    print(data.get('a'))
    print(data.get('b'))
    # 打印所有的值
    print(data.getlist('a'))
    return HttpResponse('OK')


# 获取表单数据
def form(request):
    # request.POST 包含表单数据
    data = request.POST
    print(data)
    # 打印单个值
    print(data.get('a'))
    print(data.get('b'))
    # 打印所有的值
    print(data.getlist('a'))

    # 获取查询字符串数据
    data = request.GET
    print('查询字符串数据')
    print(data)

    return HttpResponse('OK')


# 获取json
def json_data(request):
    # 1. 拿到原始数据 request.body bytes
    # 2. 转换为字符串 body.decode()
    # 3. 使用json.loads(body_str) 转化为python内置对象
    body_bytes = request.body
    body_str = body_bytes.decode()
    data = json.loads(body_str)
    print(data)
    return HttpResponse('OK')


# 请求头
def header(request):
    # request.META 包含请求头数据
    headers = request.META
    print(headers['CONTENT_LENGTH'])
    print(headers['CONTENT_TYPE'])
    return HttpResponse('OK')


# 请求对象的其他属性
def other(request):
    print('method: ', request.method)
    print('user: ', request.user)
    print('path: ', request.path)
    print('encoding: ', request.encoding)
    print('files: ', request.FILES)
    return HttpResponse('OK')


def response_view(request):
    return redirect('/users/index')
