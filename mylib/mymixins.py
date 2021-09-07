from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings

from mylib.my_common import MyCustomException, MyDjangoFilterBackend, MyIsAuthenticatedOrOptions


class MyViewMixin(object):
    filter_backends = (MyDjangoFilterBackend,)
    permission_classes = (MyIsAuthenticatedOrOptions,)

class MyCreateModelMixin(object):
    """
    Create a model instance.
    """
    object_id=None
    def create(self, request, *args, **kwargs):
        data=request.data.copy()
        data[self.foreign_key_field]=self.get_parent_id()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_parent_id(self):
        if "pk" not in self.kwargs:
            raise MyCustomException("Id is required in the url.")
        id = self.kwargs["pk"]
        if self.foreign_key_field == None:raise MyCustomException("A foreign key field is required.")
        if self.object_id != None:return self.object_id

        ##Get the parent model
        foreignmodel = self.queryset.model._meta.get_field(self.foreign_key_field).remote_field.model
        if  not foreignmodel.objects.filter(id=id).exists() :
            raise MyCustomException(foreignmodel.__name__+" does not exist.",404)
        self.object_id=id
        return id

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class SerializerCustomSerializerUpdateSave(object):
    def create(self,validated_data):
        instance=self.context.get("instance")
        return self.update(instance,validated_data)

class RetrievObjectSerializerContext(object):
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    def get_serializer_context(self):
        return {
            "request":self.request,
            "instance":self.get_object(),
            "user":self.request.user
        }

class MyUserSaveObject(object):
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

class MyListModelMixin(object):
    """
    List a queryset.
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        ##Add foreign key filtering
        queryset=queryset.filter(**{self.foreign_key_field:self.get_parent_id()})
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_parent_id(self):
        if "pk" not in self.kwargs:
            raise MyCustomException("A foreign key  is required in the url.")
        id = self.kwargs["pk"]
        if self.foreign_key_field == None: raise MyCustomException("A foreign key field is required.")
        if self.object_id != None: return self.object_id

        ##Get the parent model
        foreignmodel = self.queryset.model._meta.get_field(self.foreign_key_field).remote_field.model
        if not foreignmodel.objects.filter(id=id).exists():
            raise MyCustomException(foreignmodel.__name__ + " does not exist.", 404)
        self.object_id = id
        return id
