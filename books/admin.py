from django.contrib import admin

# Register your models here.

from .models import BookInfo, HeroInfo


class HeroInfoStackInline(admin.StackedInline):
    model = HeroInfo  # 要编辑的对象
    extra = 2  # 附加编辑的数量


class HeroInfoTabularInline(admin.TabularInline):
    model = HeroInfo
    extra = 1


class BookInfoAdmin(admin.ModelAdmin):
    # 分页
    list_per_page = 2
    # 显示的字段
    list_display = ['id', 'btitle', 'bread', 'bpub_date', 'pub_date']
    # 底部动作
    actions_on_bottom = True

    # 编辑页面定制化
    # 显示的字段
    # fields = ['btitle', 'bread', 'bpub_date', ]
    # 分组显示
    fieldsets = (
        ('基本', {'fields': ['btitle', 'bpub_date', 'image']}),
        ('高级', {
            'fields': ['bread', 'bcomment'],
            'classes': ('collapse',)  # 是否折叠显示
        })
    )
    # inlines = [HeroInfoStackInline]
    inlines = [HeroInfoTabularInline]


class HeroInfoAdmin(admin.ModelAdmin):
    # 分页
    list_per_page = 5
    list_display = ['id', 'hname', 'hgender']

    # 右侧过滤栏
    list_filter = ['hbook', 'hgender']

    # 搜索框
    search_fields = ['hname']


admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)

admin.site.site_header = '传智书城'
admin.site.site_title = '传智书城MIS'
admin.site.index_title = '欢迎使用传智书城MIS'
