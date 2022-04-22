import xadmin
from xadmin import views
from .models import ImagesPost


class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True  # 开启主题切换功能
    use_bootswatch = True


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "传统服饰识别后台管理"  # 设置站点标题
    site_footer = "传统服饰识别后台管理"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠


# 配置识别app的后台可视化
class ImagesPostModelAdmin(object):
    list_display = ["user", "nation1", "nation2", "nation3", "time_consuming", "modified_nation"]  # 需要展示的数据库字段


xadmin.site.register(views.BaseAdminView, BaseSetting)  # 全局配置注册
xadmin.site.register(views.CommAdminView, GlobalSettings)  # 全局配置注册
xadmin.site.register(ImagesPost, ImagesPostModelAdmin)  # app配置注册
