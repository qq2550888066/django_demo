from rest_framework import serializers

from book.models import BookInfo


class BookInfoSerializer1(serializers.ModelSerializer):
    """
    图书数据序列化器
    """

    class Meta:
        model = BookInfo
        fields = "__all__"

    id = serializers.IntegerField(label='ID', read_only=True)
    btitle = serializers.CharField(label='名称', max_length=20)
    bpub_date = serializers.DateField(label='发布日期', required=False)
    bread = serializers.IntegerField(label='阅读量', required=False)
    bcomment = serializers.IntegerField(label='评论量', required=False)
    image = serializers.ImageField(label='图片', required=False)