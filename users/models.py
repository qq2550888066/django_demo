from django.db import models


# Create your models here.


class Users(models.Model):  # 必须继承子models.Model
    # 属性名=models.字段类型(选项)
    name = models.CharField(max_length=32, verbose_name='名字')
