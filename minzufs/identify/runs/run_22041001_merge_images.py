import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minzufs.settings')
import django

django.setup()

from identify.models import MergedImageModel

obj: MergedImageModel = MergedImageModel.objects.last()
obj.merge()
