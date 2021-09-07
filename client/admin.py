from django.contrib import admin


# Register your models here.
from oauth2_provider.admin import Application

from client.models import MyUser, ActivityLog
from energywatchapi import settings


class AdminClass(admin.ModelAdmin):
    list_display = ["id","dummy",'username','image','reset_code','confirm_code',
                    "role"
        # ,'role','bio','gender','allow_notification','dob'
                    ]

admin.site.register(MyUser,AdminClass)


class ActivityLogAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ActivityLog._meta.get_fields() if not f.many_to_many and not f.one_to_many]
admin.site.register(ActivityLog,ActivityLogAdmin)


###Createa a superadmins
if settings.DEBUG==True:
    try:
        client_id = "fbaPXGrD6wewVEqoOkJfvierIrYbnROPXMa8CDv5"
        client_secret = "lahkckagkegiweasgciegvjegvjhd"
        user=None

        if MyUser.objects.filter(username="myadmin").exists():
            print("Making sure is admin")
            user = MyUser.objects.get(username="myadmin@gmail.com")
            user.is_staff = True
            user.is_superuser = True
            user.save()
            pass
        else:
            print("Creating super admin for test...")
            user = MyUser.objects.create_user(username="myadmin@gmail.com", email="myadmin@gmail.com", password="#myadmin")
            user.is_staff = True
            user.is_superuser = True
            user.save()

        ##Myadmin
        try:
            app = Application()
            app.name="Dev (To be deleted...)"
            app.client_id = client_id
            app.user = user
            app.authorization_grant_type = "password"
            app.client_type = "public"
            app.client_secret = client_secret
            if not Application.objects.filter(client_id=client_id).exists():
                app.save()
        except Exception as e:
            print(e)
    except:
        pass


else:
    try:
        user = MyUser.objects.get(username="myadmin@gmail.com")
        user.delete()
    except:
        pass

