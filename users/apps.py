from django.apps import AppConfig


class UsersConfig(AppConfig):
    # AppConfig.name  表示这个配置是加载到哪个应用中的
    name = 'users'
    # AppConfig.verbose_name 设置该应用的直观可读的名字,在admin管理站点会使用
    verbose_name = "用户管理"
