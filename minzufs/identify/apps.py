from django.apps import AppConfig


#  设置后端xadmin中子应用名称
class IdentifyConfig(AppConfig):
    name = 'identify'
    # 修改app名字
    verbose_name = '图片识别'
