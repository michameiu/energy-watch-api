from onesignal_sdk.client import Client

from safarinjemapi import settings

client = Client(app_id=settings.ONESIGNAL_APP_ID, rest_api_key=settings.ONESIGNAL_API_KEY)

def sendOnesignalNotification(user_ids,heading,message):
    notification_body = {
        "headings": {
            "en": heading
        },
        'contents': { 'en': message},
        'include_external_user_ids': user_ids
    }
    response = client.send_notification(notification_body)
    return  response.body
