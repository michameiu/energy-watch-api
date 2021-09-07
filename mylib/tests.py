import tempfile

from PIL import Image
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from client.models import MyUser
from oauth2_provider.models import Application


class BaseAPITest(APITestCase):
    username = "michameiu@gmail.com"
    password = "micha"
    client_id = "iuyutyutuyctua"
    client_secret = "lahkckagkegigciegvjegvjhv"
    speaker = None

    def setUp(self):
        user = MyUser.objects.create(username=self.username,first_name="Mwangi",last_name="Micha")
        self.client = APIClient()
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(user=user)
        self.user = user
        self.user.set_password(self.password)
        self.user.save()
        app = Application()
        app.client_id = self.client_id
        app.user = self.user
        app.authorization_grant_type = "password"
        app.client_type = "public"
        app.client_secret = self.client_secret
        app.save()

        ####Create a hospital staff Staff Amdin #user id 2
        resp = self.create_user()
        # print(resp.json())
        self.assertEqual(resp.status_code, 201)
        # print(resp.json())

        self.set_admin_creds()
        self.create_car_type()
        self.create_car_category()
        self.create_car_model()


        self.auth_client.force_authenticate(user=user)

    def create_car_model(self, name="madC" ):
        data={  "name":name  }
        return self.auth_client.post(reverse("list_create_car_models"),data=data)

    def create_car_category(self, name="madC" ):
        data={  "name":name  }
        return self.auth_client.post(reverse("list_create_car_categorys"),data=data)

    def get_test_image(self):
        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)
        return tmp_file

    def set_admin_creds(self):
        user1, created = MyUser.objects.get_or_create(username="admin12@gmail.com",email="admin12@gmail.com",first_name="Saf",last_name="Admin",
                                                      verified=True, role="A", phone="89738786")
        self.set_authenticated_user(user_id=user1.id)
        return user1

    def set_technician_creds(self):
        user1, created = MyUser.objects.get_or_create(username="technician@gmail.com",email="technician@gmail.com",first_name="technician",last_name="Rep",
                                                      verified=True, role="T", phone="89738796")
        self.set_authenticated_user(user_id=user1.id)
        return user1

    def create_user(self,username="mfa@gmail.com",phone="0727290364",role="N"):
        user = {"first_name": "Test","phone":phone,"email":username ,"role":role,"last_name": "Doe", "username": username, "password": "m", }
        return self.client.post(reverse("list_create_clients"), user)

    def set_authenticated_user(self,user_id=2):
        self.auth_client.force_authenticate(user=MyUser.objects.get(id=user_id))

    def create_car_type(self, _engine_capacity="1.0" , amount="1.0" , description="1" ):
        data={  "engine_capacity":_engine_capacity , "amount":amount , "description":description  }
        return self.auth_client.post(reverse("list_create_car_types"),data=data)
