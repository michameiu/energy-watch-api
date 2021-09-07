from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill, ResizeToFit
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework import serializers
from mylib.image import scramble
from mylib.mymixins import MyCreateModelMixin, MyListModelMixin, RetrievObjectSerializerContext, \
    SerializerCustomSerializerUpdateSave

from django.db import models



class MyModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        ordering=("id",)

class MyImageModel(MyModel):
    image = models.ImageField("uploads", upload_to=scramble, null=True, blank=True)
    avatar_image = ImageSpecField(source='image', processors=[ResizeToFill(360, 200)], format='WEBP',
                                  options={'quality': 80})
    main_image = ImageSpecField(source='image', processors=[ResizeToFit(height=600)], format='WEBP',
                                options={'quality': 30})
    class Meta:
        abstract=True
        ordering = ("id",)




class MyListCreateAPIView(MyCreateModelMixin,MyListModelMixin,
                    GenericAPIView):
    """
    Concrete view for creating a model instance.
    """
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class MyListAPIView(MyCreateModelMixin,MyListModelMixin,
                    GenericAPIView):
    """
    Concrete view for creating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MyUpdateSerializerContextAPIView(RetrievObjectSerializerContext,UpdateAPIView):
    pass

class CustomUpdateSerializerWithSaveUpdate(SerializerCustomSerializerUpdateSave,serializers.Serializer):
    detail=serializers.CharField(read_only=True)
    pass