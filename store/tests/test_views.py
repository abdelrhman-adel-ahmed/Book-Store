# provide a facility to skip tests (its a class decorator)
from importlib import import_module
from unittest import skip

from account.models import Customer
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from store.models import Category, Product
from store.views import product_all

"""
we need to test if the pages is loaded correclty or not ,we can do this in three ways :
1- use client class from django test module ,that acts as dummy web browser,allow us to test our views 
2- use the httprequest class to send request directly to the view
3- use advanced testing module e.x request factory 
"""

# @skip('nenenene')
# class sss(TestCase):
#     def test_skip(self):
#          pass


class TestViewResopnes(TestCase):
    def setUp(self):
        # how can i execute the clas as function ?!!!
        self.c = Client()
        self.factory = RequestFactory()
        # add some data to run the test on (especially when reverse the url we need slug data)
        Category.objects.create(name="watch", slug="watch")
        Category.objects.create(name="django", slug="django")
        Customer.objects.create(name="elshe2")
        self.data1 = Product.objects.create(category_id=1, title="watch", regular_price=12.00, slug="watch")

    def test_url_allowed_hosts(self):
        """
        test allowed hosts
        """
        respose1 = self.c.get("/", HTTP_HOST="nenene.com")
        self.assertEqual(respose1.status_code, 400)
        response2 = self.c.get("/", HTTP_HOST="127.0.0.1")
        self.assertEqual(response2.status_code, 200)

    def test_homepage_url(self):
        """
        test homepage_url
        """
        response = self.c.get("/")
        self.assertEqual(response.status_code, 200)

    def test_product_details_url(self):
        """
        test product_details url
        """
        response = self.c.get(reverse("store:product_detail", kwargs={"slug": "watch"}))
        self.assertEqual(response.status_code, 200)

    def test_category_details_url(self):
        """
        test category_details url
        """
        response = self.c.get(reverse("store:category_list", args=["django"]))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """
        send a http reqeust to the view directly and capture the repsonse,then we can analysis any thing we want
        inside the page,
        after we added session we need to send session data with the request otherwise it will cause error in the
        test so we use import_module to do that.
        """

        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = product_all(request)
        html = response.content.decode("utf8")
        self.assertInHTML("<title>Book Store</title>", html)
        self.assertEqual(response.status_code, 200)

    def test_with_request_factory(self):
        """
        request factory provide more advanced testing functionality than client class
        """

        request = self.factory.get("/watch")
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = product_all(request)
        html = response.content.decode("utf8")
        self.assertInHTML("<title>Book Store</title>", html)
        self.assertEqual(response.status_code, 200)
