from django.shortcuts import render,redirect

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
