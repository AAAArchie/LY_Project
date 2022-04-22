from django.db import models
from django.contrib.auth.models import AbstractUser


# 第一步建立用户表
class UserProfile(AbstractUser):
    
    mobile = models.CharField('手机号', max_length=11, null=True, blank=True)
    image = models.ImageField(upload_to='image/%Y%m', default='image/default.png', max_length=100)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username




