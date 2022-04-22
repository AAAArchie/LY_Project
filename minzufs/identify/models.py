import os.path
import tempfile
from pathlib import Path

from django.conf import settings
from django.db import models

from identify import lib
from users.models import UserProfile


# 数据模型
class ImagesPost(models.Model):
    # 设置null=True，则仅表示在数据库中该字段可以为空，但使用后台管理添加数据时仍然要需要输入值，因为Django自动做了数据验证不允许字段为空
    # 如果想要在Django中也可以将字段保存为空值，则需要添加另一个参数：blank=True
    # related_name可以支持 user.images_posted 直接获取一个用户的所有照片的queryset
    # 这里允许空值，因为空值可以代表用户未登录
    user = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='images_posted',
                             null=True, blank=True, default=None)

    upload_images = models.ImageField(upload_to='upload_images')  # 应该用单数
    nation1 = models.CharField(max_length=20, null=True, blank=True)
    nation2 = models.CharField(max_length=20, null=True, blank=True)
    nation3 = models.CharField(max_length=20, null=True, blank=True)
    modified_nation = models.CharField(max_length=20, null=True, blank=True)
    time_consuming = models.CharField(max_length=50, null=True, blank=True)

    # 以下为用户意见提交，无需展示到界面
    user_assess = models.CharField(max_length=50, null=True, blank=True, default='未填写')  # 用户满意程度
    user_update = models.CharField(max_length=50, null=True, blank=True, default='未修改')  # 用户更新的民族种类

    # is_changed is better
    # 其他字段都可以加一加verbose_name
    user_change = models.CharField(max_length=20, null=True, blank=True, default='否')  # 用户是否修改（不提交到前台显示）
    user_propose = models.TextField(max_length=50, null=True, blank=True, default='未填写')  # 用户建议（不提交到前台显示）
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    class Meta:
        # 模型元数据是“任何不是字段的东西”，例如排序选项(ordering)、数据库表名(db_table)
        # 或人类可读的单复数名称(verbose_name and verbose_name_plural)。
        # 不需要，并且添加到模型是完全可选的。
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 带有可选的“-”前缀，表示降序。没有前导“-”的字段将按升序排列。使用字符串“？” 随机订购。
        ordering = ('-created',)
        verbose_name = '识别结果'
        verbose_name_plural = verbose_name

    def __str__(self):
        # return self.title 将文章标题返回  __str__魔法方法，自己定义 输出打印对象时候的返回值
        return f'{self.id}'


def _merge_image_person_1_head_image_path(instance: 'MergedImageModel', filename: str):
    ext = os.path.splitext(filename)[1]
    file_name = f'merged-{instance.id}-head-1{ext}'
    return os.path.join(settings.MEDIA_ROOT, 'merge-image', file_name)


def _merge_image_person_2_head_image_path(instance: 'MergedImageModel', filename: str):
    ext = os.path.splitext(filename)[1]
    file_name = f'merged-{instance.id}-head-2{ext}'
    return os.path.join(settings.MEDIA_ROOT, 'merge-image', file_name)


def _merge_image_person_merged_path(instance: 'MergedImageModel', filename: str):
    ext = os.path.splitext(filename)[1]
    file_name = f'merged-{instance.id}-merged{ext}'
    return os.path.join(settings.MEDIA_ROOT, 'merge-image', file_name)


class MergedImageModel(models.Model):
    """
    记录了上传的用户，本次图像合成需要的参数，包括两次识别过程、两个头像、一个背景。
    """

    class Meta:
        verbose_name = '图像合成'
        verbose_name_plural = verbose_name

    user = models.ForeignKey(
        verbose_name='用户', to=UserProfile, on_delete=models.PROTECT, null=True, blank=True, default=None)
    person_1_identification = models.ForeignKey(
        verbose_name='第一个人的识别结果', to=ImagesPost, on_delete=models.PROTECT, related_name='person_1_merged_images',
        null=True, blank=True, default=None)
    person_1_head_image = models.ImageField(
        verbose_name='第一个人的头像图片', upload_to=_merge_image_person_1_head_image_path, null=True, blank=True, default=None)
    person_2_identification = models.ForeignKey(
        verbose_name='第二个人的识别结果', to=ImagesPost, on_delete=models.PROTECT, related_name='person_2_merged_images',
        null=True, blank=True, default=None)
    person_2_head_image = models.ImageField(
        verbose_name='第二个人的头像图片', upload_to=_merge_image_person_2_head_image_path, null=True, blank=True, default=None)
    background_name = models.CharField(
        verbose_name='背景名称', max_length=100, null=True, blank=True, default=None)
    result_image = models.ImageField(
        verbose_name='合成后的图片', upload_to=_merge_image_person_merged_path, null=True, blank=True, default=None)

    def save(self, *args, **kwargs):
        if not self.id:
            image1, image2 = self.person_1_head_image, self.person_2_head_image
            self.person_1_head_image, self.person_2_head_image = None, None
            super().save(*args, **kwargs)
            self.person_1_head_image, self.person_2_head_image = image1, image2
            kwargs.get('force_insert', False) is True and kwargs.pop('force_insert')
        super().save(*args, **kwargs)

    def merge(self):
        """执行图像的合并过程。"""
        head1, head2 = self.person_1_head_image.path, self.person_2_head_image.path
        clothes1, clothes2 = self.person_1_identification.upload_images.path, self.person_2_identification.upload_images.path
        background = self.background_name
        if not all((
                Path(head1).exists(), Path(head2).exists(), Path(clothes1).exists(), Path(clothes2).exists(),
                background in lib.mergeimages.BACKGROUND_LIST,
        )):
            raise ValueError(f'The image {self.id} is not available to merge now.')
        content = lib.merge_images(clothes1, head1, clothes2, head2, background)
        # try:
        #     content = lib.merge_images(clothes1, head1, clothes2, head2, background)
        # except:
        #     with open(lib.mergeimages.BACKGROUND_LIST[background], 'rb') as f:
        #         content = f.read()
        with tempfile.TemporaryFile('r+b') as f:
            f.write(content)
            self.result_image.save(f'image.png', f)
