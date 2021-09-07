from django.conf.urls import url

from client.activity_logs.views import ListActivityLogs, ExportActivityLogs
from client.views import RetrieveUpdateClient, CreateListUser, ForgotPasswordView, \
    ChangePasswordAPiView, ResetPasswordView, ResendVerifyEmailView, RetrieveUpdateUser, ResetTeacherPassword, \
    ListTechniciansAPIView

urlpatterns=[
    url(r'^$',CreateListUser.as_view(),name="list_create_clients"),
    # url(r'^logs/?$', ListActivityLogs.as_view(), name="list_activity_logs"),
    # url(r'^logs/export/?$', ExportActivityLogs.as_view(), name="export_activity_logs"),
    url(r'^me/?$',RetrieveUpdateClient.as_view(),name="retrieve_update_client"),
    url(r'^technicians/?$',ListTechniciansAPIView.as_view(),name="list_technicians"),
    # url(r'^(?P<pk>[0-9]+)/?$',RetrieveUpdateUser.as_view(),name="retrieve_update_client"),
    url(r'^me/profile/?$',RetrieveUpdateClient.as_view(),name="Retrieve_client"),
    # url(r'^me/change-password', ChangePasswordAPiView.as_view(), name="clients_change_password"),
    # url(r'^me/resend-verification-email', ResendVerifyEmailView.as_view(), name="clients_resend_confirm_email"),
    url(r'^forgot-password', ForgotPasswordView.as_view(), name="clients_forgot_password"),
    url(r'^reset-password', ResetPasswordView.as_view(), name="clients_reset_password"),
    # url(r'^admin-reset-password/?$', ResetTeacherPassword.as_view(), name="admin_reset_enum_password"),
]