from django.contrib.auth import authenticate
from django.test import TestCase
from .models import *
from .views import *

# from unittest import TestCase
class RequestCLass():
    def __init__(self, **kwargs):
        user = kwargs['user']

class SimpleTest(TestCase):
    # def test_1(self):
    #     self.assertEqual("1", str(1))

    def test_create_prod(self):
        cat = PCategories(name='TestingCat')
        cat.save()
        self.assertIsInstance(cat,PCategories)
        prod = Products(name='testProd',
                        factory='TestFactory',
                        p_text='Test text',
                        image='media/prod_none.png',
                        balance=5,
                        coast=1000.00,
                        cat_id = cat.pk)
        prod.save()
        self.assertIsInstance(prod,Products)
        return [prod, cat]

    def test_create_client(self):
        usr = User(username='TestLogin', password='1234qwerASDF')
        usr.save()
        self.assertIsInstance(usr, User)
        det_usr = Clients(user_id=usr.pk,
                           address='TestAddress',
                           phone='TestPhone')
        det_usr.save()
        self.assertIsInstance(det_usr, Clients)
        return [usr, det_usr]

    # def test_create_order(self):
    #
    #     prod, cat = self.test_create_prod()
    #     usr, det_usr = self.test_create_client()
    #     self.assertIsInstance(prod, Products)
    #     self.assertIsInstance(cat, PCategories)
    #     self.assertIsInstance(usr, User)
    #     self.assertIsInstance(det_usr, Clients)
    #     user = authenticate(username='TestLogin', password='1234qwerASDF')
    #     req = RequestCLass(user=usr)
    #     add_box( self.request, prod.pk)
    #     order=Orders.objects.filter(user_id=usr.pk)
    #     self.assertTrue(order)