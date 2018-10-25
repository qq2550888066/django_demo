import json
import datetime

# 安装的第三方包
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# 导入自己的包

# Create your views here.
# flask 定义视图函数
# @app.router(路径,methods=[,])
# def index():
#     return 'hello world'
from django.template import loader
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View


def index(request):  # 必须传递request参数,封装客户请求数据,HttpRequest对象

    # raise Exception('test')
    # 必须返回一个HttpResponse对象
    return HttpResponse('hello world')


def index1(request):
    # 查询index2路由名称对应的路径
    # 没有添加namespace
    # path = reverse('index2')
    # 添加namespace之后
    path = reverse('users:index2')
    print(path)
    return HttpResponse('index1')


def index2(request):
    return HttpResponse('index2')


# request.args 查询字符串数据 /users/index?a=1&b=2&a=3&c=4

# request.form 表单数据 请求体数据
# request.json json数据 请求体数据
# request.files 文件 请求体数据
# request.data 纯文本 请求体数据

# request.headers 请求头数据

# users/1
# app.route('users/<id>',...)
# 路径中的信息
# weather/beijing/2018 表示获取北京2018年天气情况
# weather/shandong/2017 表示获取山东2017年天气情况

# URL获取数据
def weather(request, city, year):
    # weather(,city,year)
    # 使用分组时,有几个分组就会向函数中传递几个参数
    # 而且传递的顺序与分组顺序一致
    print('city: ', city)
    print('year: ', year)

    return HttpResponse('OK')


def weather_named(request, year, city):
    # weather_named(,city=city,year=year)
    # 参数顺序不再重要
    print('city: ', city)
    print('year: ', year)

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


# 构建响应
def create_response(request):
    # 创建响应对象
    response = HttpResponse(content='创建响应', content_type='text/plain', status=201)

    response['Itcast'] = 'python'

    return response


# 构建json字符串
def create_json(request):
    data = {
        "a": 10,
        "b": 20
    }
    data_list = [1, 2, 3]
    # 手动构建json响应
    # json_str = json.dumps(data)
    # response = HttpResponse(content=json_str, content_type='application/json')

    # 使用JsonResponse构建json响应
    # response = JsonResponse(data)
    # 如果返回列表数据 那么要添加safe=False
    response = JsonResponse(data_list, safe=False)
    return response


# 重定向
def redirect_response(request):
    # 重定向使用完整路径
    return redirect('/users/index')


# 设置cookie
def set_cookie(request):
    response = HttpResponse(content='设置cookie')
    # 设置cookie
    response.set_cookie('cookie_key', 'cookie_value')
    return response


def read_cookie(request):
    cookies = request.COOKIES
    print(cookies)
    return HttpResponse("OK")


# 设置session值
def set_session(request):
    # 拿到客户对应的session字典
    session = request.session

    session['test'] = 'value'
    session['test1'] = 'value1'
    session['test2'] = 'value2'
    session['test3'] = 'value3'
    session['test4'] = 'value4'
    session.set_expiry(5)

    return HttpResponse('Ok')


# 读取session值
def read_session(request):
    session = request.session
    # 清楚session数据
    # session.clear()
    #
    print(session.get('test', 'none'))
    # 删除session
    # session.flush()
    return HttpResponse('OK')


# method path version : GET /users/index HTTP/1.1
# GET,POST,PUT,DELETE
#
# GET: 查询数据
# POST: 创建数据
# PUT: 更新数据
# DELETE: 删除数据

def user(request):
    #     操作user数据库表
    method = request.method
    if method == 'GET':
        # 查询用户信息
        return HttpResponse('get')
    elif method == 'PUT':
        # 更新用户信息
        return HttpResponse('put')
    elif method == 'POST':
        # 更新用户信息
        return HttpResponse('post')
    elif method == 'DELETE':
        # 更新用户信息
        return HttpResponse('delete')
    else:
        return HttpResponse('未知的请求方法')


# 自定义装饰器
def my_decorator(func):
    def wrapper(request, *args, **kwargs):
        print('自定义装饰器被调用了')
        print('请求路径%s' % request.path)
        return func(request, *args, **kwargs)

    return wrapper


# 自定义装饰器2
# def my_decorator2(func):
#     def wrapper(request, *args, **kwargs):
#         print('自定义装饰器被调用了')
#         print('请求路径%s' % request.path)
#         return func(request, *args, **kwargs)
#     return wrapper


@my_decorator
def goods(request):
    pass


my_decorator(goods)


# @method_decorator(my_decorator, name='dispatch') # 全部方法装饰
@method_decorator(my_decorator, name='get')  # 只对get方法
class DemoView(View):

    # @method_decorator(my_decorator)
    def get(self, request):
        return HttpResponse('get')

    def post(self, request):
        return HttpResponse('post')

    def put(self, request):
        return HttpResponse('put')

    def delete(self, request):
        return HttpResponse('delete')


class CreateMixin(object):
    def create(self):
        # 执行创建数据操作
        return HttpResponse('创建成功')


class UpdateMixin(object):
    def update(self):
        # 执行更新数据操作
        return HttpResponse('更新成功')


class ListMixin(object):
    def list(self):
        # 执行查询数据操作
        return HttpResponse('查询成功')


class DeleteMixin(object):
    def drop(self):
        # 执行删除数据操作
        return HttpResponse('删除成功')


class DemoView2(ListMixin, DeleteMixin, View):
    def get(self, request):
        return self.list()

    def delete(self, request):
        return self.drop()


class DemoView3(ListMixin, CreateMixin, View):
    def get(self, request):
        return self.list()

    def post(self, request):
        return self.create()


def render_template(request):
    # 获取模板
    template = loader.get_template('index.html')
    # 构建上下文
    # context = {
    #     "city": '北京'
    # }
    # html = template.render(context)
    # return HttpResponse(html)
    # context = {
    #     "city": '北京'
    # }

    context = {
        'city': '北京',
        'adict': {
            'name': '西游记',
            'author': '吴承恩'
        },
        'alist': [1, 2, 3, 4, 5]
    }
    # 第一个request必须传递,第二个模板名字,第三个上下文
    return render(request,'index.html',context)
