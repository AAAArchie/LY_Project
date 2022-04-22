from django import forms
from .models import ImagesPost,ImagesPostLog

class ImageForm(forms.ModelForm):

    class Meta:
        model = ImagesPost
        fields = ['upload_images']

#
# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         model = ImagesModify
#         fields = ['user_update','user_change','user_assess','user_propose']
#

class ImagesPostLogForm(forms.ModelForm):

    class Meta:
        model = ImagesPostLog
        fields = ['upload_images']