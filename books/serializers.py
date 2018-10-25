from rest_framework import serializers

from books.models import BookInfo, HeroInfo


class BookInfoSerializer(serializers.ModelSerializer):
    """图书数据序列化器"""

    class Meta:
        model = BookInfo
        fields = '__all__'


def about_python(value):
    print('about_python')
    if 'python' not in value.lower():
        raise serializers.ValidationError("图书不是关于Python的")


class BookInfoSerializerTest(serializers.Serializer):
    """图书数据序列化器"""
    id = serializers.IntegerField(label='ID', read_only=True)
    btitle = serializers.CharField(label='名称', max_length=20, validators=[about_python])
    bpub_date = serializers.DateField(label='发布日期', required=False)
    bread = serializers.IntegerField(label='阅读量', required=False)
    bcomment = serializers.IntegerField(label='评论量', required=False)
    image = serializers.ImageField(label='图片', required=False)

    # heroinfo_set = serializers.PrimaryKeyRelatedField(label='图书', read_only=True, many=True)
    heroinfo_set = serializers.StringRelatedField(label='图书', read_only=True, many=True)

    example = serializers.SerializerMethodField()

    def get_example(self, obj):
        return obj

    # validate_字段(self,客户端传递值):
    # 如果验证失败 需要抛出serializers.ValidationError
    # 若果成功直接返回 客户端传递值
    def validate_btitle(self, value):
        print('validate_btitle')
        if 'django' not in value.lower():
            raise serializers.ValidationError("图书不是关于Django的")
        return value

    # 联合校验
    def validate(self, attrs):
        print('validate')
        if attrs['bread'] < attrs['bcomment']:
            raise serializers.ValidationError('阅读量小于评论量')

        return attrs

    def create(self, validated_data):
        """新建"""
        return BookInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        instance.btitle = validated_data.get('btitle', instance.btitle)
        instance.bpub_date = validated_data.get('bpub_date', instance.bpub_date)
        instance.bread = validated_data.get('bread', instance.bread)
        instance.bcomment = validated_data.get('bcomment', instance.bcomment)
        instance.save()
        return instance


class HeroInfoSerializer(serializers.Serializer):
    """英雄数据序列化器"""
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    id = serializers.IntegerField(label='ID', read_only=True)
    hname = serializers.CharField(label='名字', max_length=20)
    hgender = serializers.ChoiceField(choices=GENDER_CHOICES, label='性别', required=False)
    hcomment = serializers.CharField(label='描述信息', max_length=200, required=False, allow_null=True)

    # 返回的是hbook_id
    # hbook = serializers.PrimaryKeyRelatedField(label='图书', read_only=True)
    # hbook.__str__()
    # hbook = serializers.StringRelatedField(label='图书')
    # BookInfoSerializerTest(instance=hero.hbook).data
    # hbook = BookInfoSerializerTest()


# 普通用户
class BookInfoSerializer(serializers.Serializer):
    btitle = serializers.CharField(label="书名")
    bpub_date = serializers.DateField(label="出版时间")


# 管理员
class BookInfoSerializerFull(serializers.Serializer):
    id = serializers.IntegerField(label="ID")
    btitle = serializers.CharField(label="书名")
    bpub_date = serializers.DateField(label="出版时间")
    bread = serializers.IntegerField(label="阅读量")
    bcomment = serializers.IntegerField(label="评论量")
    is_delete = serializers.BooleanField(label="是否删除")

    # 返回的是关联对象的id列表
    # heroinfo_set=serializers.PrimaryKeyRelatedField(label="所有英雄",many=True,read_only=True)
    # 返回的是关联对象的__str__()返回值 列表
    heroinfo_set = serializers.StringRelatedField(label="所有英雄", many=True, read_only=True)


# 英雄序列化器

class HeroInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID')
    hname = serializers.CharField(label="姓名")
    hgender = serializers.IntegerField(label="性别")
    hcomment = serializers.CharField(label="介绍")
    is_delete = serializers.BooleanField(label="是否删除")

    # 返回的是  关联对象.id
    # hbook = serializers.PrimaryKeyRelatedField(label="所在书籍", read_only=True)
    # 返回的是 关联对象.__str__()
    # hbook=serializers.StringRelatedField(label="所在书籍",read_only=True)
    # 不传递 instance 或者 data
    # 返回的是 BookInfoSerializer(hero.hbook).data
    # hbook = BookInfoSerializer()


def about_django(value):
    # value 是对应客户端传递进来的字段值
    # 判断value适合合法
    # 不合法的时候,必须抛出 serializers.ValidationError('错误具体信息')
    # 如何合法 那么就返回 None
    if 'django' not in value:
        raise serializers.ValidationError('这本书不是关于django的')
    return None


# 普通管理员
class BookInfoSerializerCreate(serializers.Serializer):
    btitle = serializers.CharField(label="书名", min_length=1, max_length=32, validators=[about_django])
    bpub_date = serializers.DateField(label="出版时间")
    bread = serializers.IntegerField(label="阅读量", default=1)
    bcomment = serializers.IntegerField(label="评论量", default=1, required=False)

    # 1. 先验证的是 validators
    # 2. validate_{字段名}(self,value)
    # 3. validate(self)
    # def validate_{字段名}(self,value)
    def validate_btitle(self, value):
        # value 是对应客户端传递进来的字段值
        # 判断是否合法
        # 不合法的时候,必须抛出 serializers.ValidationError('错误具体信息')
        # 如何合法 必须返回value
        if 'python' not in value:
            raise serializers.ValidationError('这本书不是关于python的')
        return value

    def validate(self, attrs):
        # attrs原始数据
        bread = attrs.get('bread', 1)
        bcomment = attrs.get('bcomment', 1)
        # 不合法的时候,必须抛出 serializers.ValidationError('错误具体信息')
        if bread < bcomment:
            raise serializers.ValidationError('阅读量不可以小于评论量')
        # 如何合法 必须返回attrs
        return attrs

    # 创建对象
    def create(self, validated_data):
        return BookInfo.objects.create(**validated_data)

    # 更新对象
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def save(self):
        if self.instance:
            return self.update(self.instance, self.validated_data)
        else:
            return self.create(self.validated_data)


# 管理员
class BookInfoSerializerCreateFull(serializers.Serializer):
    btitle = serializers.CharField(label="书名", min_length=1, max_length=32)
    bpub_date = serializers.DateField(label="出版时间")
    bread = serializers.IntegerField(label="阅读量", default=1, required=False)
    bcomment = serializers.IntegerField(label="评论量", default=1, required=False)
    is_delete = serializers.BooleanField(label="是否删除", default=False, required=False)


# 模型类序列化器
class ModelsSerializerBookInfo(serializers.ModelSerializer):
    heroinfo_set = serializers.StringRelatedField(many=True, label="所有英雄")

    class Meta:
        model = BookInfo
        # 自动添加所有字段
        # fields = '__all__'
        # 指明具体的字段列表
        fields = ['id', 'btitle', 'bpub_date', 'heroinfo_set', 'bread']
        # 排除字段 和 fields不能同时使用
        # exclude = ['image']
        # 指明那些字段是只读的
        read_only_fields = ['is_delete', 'btitle']
        extra_kwargs = {
            "bread": {
                "min_value": 1,
                "required": True
            },
            "bcomment": {
                "max_value": 1024,
            }
        }


class ModelsNormalSerializerBookInfo(serializers.ModelSerializer):
    class Meta:
        model = BookInfo
        fields = ['id', 'btitle', 'bpub_date']
        extra_kwargs = {
            'bpub_date': {
                "help_text": "出版时间"
            }
        }
