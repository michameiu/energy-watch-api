from datetime import timedelta

import django_filters
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet
from oauth2_provider.models import AccessToken, RefreshToken,Application
from oauth2_provider.settings import oauth2_settings
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission

from energywatchapi.settings import DEFAULT_FROM_EMAIL
from django.db import models
from oauthlib import common
from django.utils import timezone
class MyCustomException(APIException):
    status_code = 503
    detail = "Service temporarily unavailable, try again later."
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'

    def __init__(self, message, code=400):
        self.status_code = code
        self.default_detail = message
        self.detail = message


def get_digitalocean_spaces_download_url(filepath):
    # client = boto3.Session.client(boto3.Session(), 's3',
    #                               region_name=AWS_S3_REGION_NAME,
    #                               # endpoint_url=AWS_S3_ENDPOINT_URL,
    #                               aws_access_key_id=AWS_ACCESS_KEY_ID,
    #                               aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    #                               )
    # url = client.generate_presigned_url(ClientMethod='get_object',
    #                                     Params={'Bucket':AWS_STORAGE_BUCKET_NAME ,
    #                                             'Key': filepath},
    #                                     ExpiresIn=3000)
    return ""


def generateUserToken(activated_user):
    default_client_id="kadkmalkm218n21b9721u2ji12"
    default_client_secret="ueiuuew893iueiwyeiuwyiu"
    application = Application.objects.get_or_create(client_id=default_client_id,
                                                    name="autoLogin",
                                                    authorization_grant_type="password",
                                                    client_type="public",
                                                    client_secret=default_client_secret
                                                    )
    application=application[0]
    expires = timezone.now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    access_token = AccessToken(
        user=activated_user,
        scope='',
        expires=expires,
        token=common.generate_token(),
        application=application
    )
    access_token.save()
    refresh_token = RefreshToken(
        user=activated_user,
        token=common.generate_token(),
        application=application,
        access_token=access_token
    )
    refresh_token.save()
    return {
        "access_token":access_token.token,
        "refresh_token":refresh_token.token,
        "token_type":"Bearer",
        "expires_in":oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS
    }


class MyDjangoFilterBackend(DjangoFilterBackend):
    myfilter_class = None

    def get_filter_class(self, view, queryset=None):
        """
        Return the django-filters `FilterSet` used to filter the queryset.
        """
        if self.myfilter_class:
            return self.myfilter_class

        queryset = getattr(view, 'queryset', None)
        extra_fields=getattr(view,'extra_filter_fields',None)

        try:
            model = queryset.model
            filter_model = model
            ##print"The filter class ...")
            filter_class = self.get_dynamic_filter_class(model,extra_fields=extra_fields)
            ##print"The filter class ...")
            assert issubclass(queryset.model, filter_model), \
                'FilterSet model %s does not match queryset model %s' % \
                (filter_model, queryset.model)
            self.myfilter_class = filter_class
            return filter_class
        except Exception as e:
            print(e)
            raise MyCustomException("Dynamic Filter class error.")

    def get_dynamic_filter_class(self, model_class,extra_fields=None):
        class Meta:
            model = model_class
            exclude = ('file','plate_number_image','before_image' , 'image','recording',"logo","avatar","location")  # [f.name for f in model_class.fields if  f.name in ["logo","image","file"]]
            fields = ("__all__")
            filter_overrides = {
                models.CharField: {
                    'filter_class': django_filters.CharFilter,
                    'extra': lambda f: {
                        'lookup_expr': 'icontains',
                    },
                }
            }

        attrs = {"Meta": Meta,}

        ##Append the extraFields
        if extra_fields:
            for field in extra_fields:
                extra_field=self.get_etxra_fields(**field)
                if extra_field:attrs[field["field_name"]]=extra_field

        filter_class = type(model_class.__class__.__name__ + "FilterClass", (FilterSet,), attrs)
        return filter_class

    def get_etxra_fields(self,field_name,label,field_type,lookup_expr="exact"):
        if field_type=="number" :
            return django_filters.NumberFilter(field_name=field_name,label=label,lookup_expr=lookup_expr)
        elif field_type=="char":
            return django_filters.CharFilter(field_name=field_name,label=label,lookup_expr="icontains")
        elif field_type=="date":
            return django_filters.DateFilter(field_name=field_name,label=label,lookup_expr=lookup_expr)
        elif field_type=="datetime":
            return django_filters.DateTimeFilter(field_name=field_name,label=label,lookup_expr=lookup_expr)
        else:
            return None



"""
from mylib.my_common import MySendEmail as se

data={"verify_url":"Micha","name":"mwangi Micha","old_password":"hello"}
se("Test email","new_user.html",data,["michameiu@gmail.com"])

"""
def MySendEmail(subject, template, data, recipients, from_email=None):
    if from_email == None:from_email=DEFAULT_FROM_EMAIL
    rendered = render_to_string(template, data)
    # print("Sending email...")
    ema = send_mail(
        subject=subject,
        message="",
        html_message=rendered,
        from_email=from_email,
        recipient_list=recipients,  # ['micha@sisitech.com'],
        fail_silently=False,
        # reply_to="room@katanawebworld.com"
    )
    return ema


class MyStandardPagination(PageNumberPagination):
    page_size = 100
    max_page_size = 1000
    page_size_query_param = 'page_size'


class MyIsAuthenticatedOrOptions(BasePermission):
    safe_methods = ["OPTIONS", ]

    def has_permission(self, request, view):
        if request.method in self.safe_methods:
            return True
        return request.user.is_authenticated()


def str2bool(value):
    trues = ["yes", "true", "1"]
    if value and value.lower() in trues:
        return True
    return False


def get_get_next_stage(previous_stage):
    stages=[d[0] for d in FORM_STAGES]
    index=stages.index(previous_stage)
    next_index=index+1 if index < len(stages) else index
    # print("{} ==> {}".format(previous_stage, next_index))
    return stages[next_index]


