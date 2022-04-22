import os
from pathlib import Path

import rest_framework.pagination
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import mixins, exceptions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from users.models import UserProfile
from .models import ImagesPost, MergedImageModel
from .rename import BatchRename
from .serializer import ImagesPostLogSerializerV2, MergedImageSerializer


class ImagesPostViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = ImagesPost.objects.all()
    serializer_class = ImagesPostLogSerializerV2
    permission_classes = [AllowAny]
    # 让DRF可以识别图片，解析器
    # 解析器的作用就是服务端接收客户端传过来的数据，把数据解析成自己想要的数据类型的过程。本质就是对请求体中的数据进行解析。
    # 就是拿到请求的ContentType来判断前端给我的数据类型是什么，然后我们去拿相应的解析器去解析数据。
    parser_classes = [JSONParser, FormParser, MultiPartParser, FileUploadParser]

    def get_queryset(self):
        """
        # queryset-应该用于从该视图返回对象的查询集。通常，您必须设置此属性或重写get_queryset()方法。
        # 如果要覆盖视图方法，则应进行调用get_queryset()而不是直接访问此属性，这一点很重要，
        # 因为queryset它将被评估一次，并且这些结果将被缓存用于所有后续请求，这一点很重要
        """
        user: UserProfile = self.request.user
        if isinstance(user, AnonymousUser):
            return ImagesPost.objects.filter(user__isnull=True)
        return ImagesPost.objects.filter(user=user).all()

    def perform_create(self, serializer: ImagesPostLogSerializerV2):
        """
        创建一张照片，并进行识别
        """
        super(ImagesPostViewSet, self).perform_create(serializer)
        instance: ImagesPost = serializer.instance
        instance.user = None if isinstance(self.request.user, AnonymousUser) else self.request.user
        # 实例化重命名BatchRename()模块  运行predict.py与rename.py
        batch_rename = BatchRename()
        # 提取相应的返回值
        nation1, nation2, nation3, dst, time_consuming = batch_rename.rename()
        # dst：图片重新分类后保存的路径  new_url 截取的相对路径
        instance.upload_images = os.path.relpath(dst, settings.MEDIA_ROOT)
        # 类别
        instance.nation1 = nation1
        instance.nation2 = nation2
        instance.nation3 = nation3
        instance.time_consuming = time_consuming  # 耗费的时间
        instance.save()

    # 修改民族类别 @action 额外的路由方法（drf视图集）
    @action(detail=True, url_path='change-nation', url_name='change-nation', methods=['GET'])
    def change_nation(self, request: Request, pk: str):
        """"
        # 前端通过/images/23/change_nation可以调用这个方法
        # 使用action装饰器
        # methods:支持的请求方式，为一个列表，默认为[‘get’]
        # detail:必传参数，要处理的是否是详情资源对象（即是否通过url路径获取主键），True表示需要传递主键id，使用通过URL获取的主键对应的数据对象，False表示不需要传递主键id，不使用URL获取主键
        # url_path:指定url路由名称，默认为action名称
        # url_name:指定url的名称，默认为action名称
        """
        instance: ImagesPost = self.get_object()
        try:
            # 获取字段名字
            name = request.query_params['name']

        except MultiValueDictKeyError:
            raise exceptions.ValidationError('参数name不存在')
        instance.modified_nation = name
        instance.save()
        return self.retrieve(request)

    # 用户提交建议
    @action(detail=True, url_path='user-assess', url_name='user-assess', methods=['GET'])
    def user_assess(self, request: Request, pk: str):
        instance: ImagesPost = self.get_object()
        try:
            name = request.query_params['assess']

        except MultiValueDictKeyError:
            raise exceptions.ValidationError('参数name不存在')
        instance.user_assess = name
        instance.save()
        return self.retrieve(request)


class MergedImagePagination(rest_framework.pagination.LimitOffsetPagination):
    max_limit = 50
    default_limit = 100


class MergedImageViewSet(viewsets.ModelViewSet):
    """
    对前端的逻辑进行整理，后端应当配合前端进行实现。

    最开始的入口点时： ``/image-merge/``

    这个时候，后面没有 ``id`` ，因此对其进行任何操作都是直接使用 ``create`` 方法生成一个新的对象。

    比如，此时用户上传了一个头像，那么直接创建对象，并简单的保存下来这个头像。这里通过 ``POST`` 进行上传。

    比如，此时用户上传了一个需要识别的服饰，那么进行识别，创建一个对象，通过 ``POST`` 创建对象，指定主键进行关联。
        也就是说，前端直接调用服饰识别的接口，然后将识别过程的主键发送到后端。

    此时对象已经创建，页面进行跳转： ``/image-merge/326/``
    由于存在了 ``id`` ，因此后续的所有内容都是对其进行编辑，是 ``patch`` 操作，包括上传第二个图片的信息等操作。

    数据完全上传完成之后，前端调用 ``merge`` 这个 ``action`` ，实现图像的合成。
    合成后的图像存在相应的的字段里面。
    """

    def get_queryset(self):
        return MergedImageModel.objects.order_by('-id').filter(user=self.request.user)

    serializer_class = MergedImageSerializer
    pagination_class = MergedImagePagination

    @action(detail=True, url_name='merge', url_path='merge')
    def merge(self, request: Request, pk):
        obj: MergedImageModel = self.get_object()
        obj.merge()
        return redirect('merged-images-detail', obj.id)

    @action(detail=False, url_name='travelled', url_path='travelled')
    def travelled(self, request: Request):
        qs = self.get_queryset().exclude(result_image__exact=None).order_by('-id')
        backgrounds = {}
        [backgrounds.setdefault(o.background_name, o) for o in qs
         if o.result_image and Path(o.result_image.path).exists()]
        qs = self.get_queryset().filter(id__in=[o.id for o in backgrounds.values()])

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
