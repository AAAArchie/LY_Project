from rest_framework import serializers
from rest_framework.request import Request

from identify.models import ImagesPost, MergedImageModel


class ImagesPostLogSerializerV2(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.SlugRelatedField('username', read_only=True)
    nation1 = serializers.CharField(read_only=True)
    nation2 = serializers.CharField(read_only=True)
    nation3 = serializers.CharField(read_only=True)
    modified_nation = serializers.CharField(read_only=True)
    upload_images = serializers.ImageField()
    time_consuming = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ImagesPost
        fields = ["id", "user", "upload_images", "nation1", "nation2", "nation3", 'modified_nation', "time_consuming",
                  "created", 'modified']


_image_post_queryset = ImagesPost.objects.all()


class MergedImageSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField('username', read_only=True)
    person_1_identification = serializers.PrimaryKeyRelatedField(queryset=_image_post_queryset, allow_null=True,
                                                                 allow_empty=True, default=None)
    person_2_identification = serializers.PrimaryKeyRelatedField(queryset=_image_post_queryset, allow_null=True,
                                                                 allow_empty=True, default=None)
    person_1_head_image = serializers.ImageField(allow_null=True, allow_empty_file=True, default=None)
    person_2_head_image = serializers.ImageField(allow_null=True, allow_empty_file=True, default=None)
    person_1_identification_detail = ImagesPostLogSerializerV2(source='person_1_identification', read_only=True)
    person_2_identification_detail = ImagesPostLogSerializerV2(source='person_2_identification', read_only=True)
    result_image = serializers.ImageField(read_only=True)
    detail_url = serializers.HyperlinkedIdentityField(view_name='merged-images-detail')

    class Meta:
        model = MergedImageModel
        fields = ['id', 'user', 'detail_url', 'background_name', 'result_image',
                  'person_1_head_image', 'person_2_head_image',
                  'person_1_identification', 'person_2_identification',
                  'person_1_identification_detail', 'person_2_identification_detail', ]

    def create(self, validated_data):
        request: Request = self.context.get('request')
        validated_data = {**validated_data, 'user': request.user}
        return super().create(validated_data)
