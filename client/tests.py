from django.test import TestCase, tag

# Create your tests here.
from oauth2_provider.models import Application
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase, APIRequestFactory

from client.models import MyUser


class CLientTest(APITestCase):
    username = "michameiu@gmail.com"
    password = "micha"
    client_id = "iuyutyutuyctua"
    client_secret = "lahkckagkegigciegvjegvjhv"
    speaker=None

    def setUp(self):
        user = MyUser.objects.create(username=self.username)
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.user = user
        self.user.set_password(self.password)
        self.user.save()
        self.cl = APIClient()
        app= Application()
        app.client_id=self.client_id
        app.user=self.user
        app.authorization_grant_type="password"
        app.client_type="public"
        app.client_secret=self.client_secret
        app.save()

    def set_admin_creds(self):
        user1, created = MyUser.objects.get_or_create(username="admin12@gmail.com",email="admin12@gmail.com",first_name="Saf",last_name="Admin",
                                                      verified=True, role="A", phone="89738786")
        self.client.force_authenticate(user1)
        # self.set_authenticated_user(user_id=user1.id)

    def create_user(self):
        user = {"first_name": "Test",
                "phone":"0727290364","email":"test@gmail.com", "last_name": "Doe", "username": "kel", "password": "m"}
        cl=APIClient()
        return cl.post(reverse("list_create_clients"),user)

    def get_token(self,username="test@gmail.com",password="m"):
        # user={"username":"kel","password":"m","client_id":self.client_id,"grant_type":"password"}
        user="username={2}&password={1}&client_id={0}&grant_type=password".format(self.client_id,password,username)
        data={"username":username,"password":password,"grant_type":'password',"client_id":self.client_id}
        cl = APIClient()
        return cl.post("/auth/token/",data)


        # print(resp)

    def test_creating_user(self):
        resp=self.create_user()
        self.assertTrue("profile" in resp.json())
        self.assertTrue("token" in resp.json())
        self.assertEqual(resp.status_code,201)
        token=resp.json()["token"]["access_token"]

        cl = APIClient()
        cl.credentials(HTTP_AUTHORIZATION="Bearer %s" % (token))
        resp = cl.get(reverse("retrieve_update_client"))
        self.assertEquals(resp.status_code,200)
        # print(resp.json())

    @tag('ltechsf')
    def test_listing_technicians(self):
        resp = self.client.get(reverse("list_technicians"))
        print(resp.json())
        self.assertEqual(resp.status_code, 403)

    @tag('ltechs')
    def test_listing_technicians(self):
        self.set_admin_creds()
        resp = self.client.get(reverse("list_technicians"))
        print(resp.json())
        self.assertEqual(resp.status_code, 200)
        self.assertEquals(resp.json()["count"],0)


    def test_retriving_profile(self):
        # resp = self.create_user()
        resp=self.client.get(reverse("retrieve_update_client"))
        # print(resp.json())
        self.assertEqual(resp.status_code,200)


    @tag("login")
    def test_login_user(self):
        resp=self.create_user()
        # print(resp.json())
        username=resp.json()["profile"]["username"]
        resp=self.get_token(username=username,password="m")
        # print(resp.json())
        token=resp.json()["access_token"]
        cl=APIClient()
        cl.credentials(HTTP_AUTHORIZATION="Bearer %s"%(token))
        resp=cl.get(reverse("retrieve_update_client"))
        # print(resp)
        self.assertEqual(resp.status_code,200)
        # print(resp)
        # pass



    def test_retrieving_chart_setting(self):
        # resp=self.client.get(reverse("Retrieve_client"))
        # print(resp.json())
        pass

    #
    # def test_change_password_wrong_password(self):
    #     data={"old_password":"ma","new_password":"m"}
    #     resp=self.client.put(reverse("clients_change_password"),data)
    #     # print(resp)
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    #
    #
    # def test_change_password_correct_password(self):
    #     data={"old_password":"micha","new_password":"mic"}
    #     resp=self.client.put(reverse("clients_change_password"),data)
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)
    #
    def test_forgot_password_wrong_email(self):
        data={"email":"michame@gmail.com"}
        cl = APIClient()
        resp=cl.post(reverse("clients_forgot_password"),data)
        # print(resp)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


    def test_forgot_password_correct_email(self):
        data={"email":self.username}
        cl = APIClient()
        resp = cl.post(reverse("clients_forgot_password"), data)
        # print(resp)

    def test_resetting_password(self):
        self.test_forgot_password_correct_email()
        new_password = "ppppaaaa"
        username="michameiu@gmail.com"
        reset_code=MyUser.objects.get(username=username).reset_code
        data={"new_password":new_password,"reset_code":reset_code}
        resp=self.cl.post(reverse("clients_reset_password"),data)
        # print(resp)
        self.assertEqual(resp.status_code,200)
        resp=self.get_token(username=username,password=new_password)
        # print(resp)
        self.assertEqual(resp.status_code,200)



    def test_social_login_google(self):
        data={"token":"ya29.GluXBkvR5OT2V4T-TPYhG4JHXAo2u5LJO8AEKqr3kXJj-A43wQsJVjq35lPhscRjvfaz8SsY9wm5HMpCZxxAUhsq_6CHT6EYqRydqgqYjwsrWMEYcXrKDqMhDKB6",
              "backend":"google-plus",
                "grant_type":"convert_token",
              "client_id":self.client_id
              }
        resp=self.client.post("/auth/convert-token",data=data)








