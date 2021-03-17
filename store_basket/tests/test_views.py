from decimal import Decimal

from account.models import Customer
from django.test import TestCase
from django.urls import reverse
from store.models import Category, Product


class TestBasketView(TestCase):
    def setUp(self):
        Customer.objects.create(user_name="admin")
        Category.objects.create(name="watch", slug="watch")
        Category.objects.create(name="django", slug="django")
        Category.objects.create(name="math", slug="math")

        Product.objects.create(category_id=1, title="watch", price=12.00, created_by_id=1, image="watch", slug="watch")
        Product.objects.create(
            category_id=2, title="django", price=19.00, created_by_id=1, image="django", slug="django"
        )
        Product.objects.create(category_id=3, title="math", price=20.00, created_by_id=1, image="math", slug="math")

        shipping = Decimal(11.50)
        # post takes: url, data to the front end(associated with the url ajax call) ,
        # the type of request we using wich is xhr (xmlHttpRequest).
        self.client.post(
            reverse("store_basket:basket_add"), {"productid": 1, "productqty": 2, "action": "post"}, xhr=True
        )
        self.client.post(
            reverse("store_basket:basket_add"), {"productid": 2, "productqty": 4, "action": "post"}, xhr=True
        )

    def test_basket_url(self):
        """
        test basket summary url
        """
        response = self.client.get(reverse("store_basket:basket_summary"))
        self.assertEquals(response.status_code, 200)

    def test_basket_add(self):
        """
        test basket add functionality.
        basket_add function return json payload contain the qty of the basket.
        """
        # note: we added two item to the session data in the setup function the new qty for productid 1 will
        # be overwritten and the total qty will be 1+4 because it already exists so it enter the else part
        response1 = self.client.post(
            reverse("store_basket:basket_add"), {"productid": 1, "productqty": 1, "action": "post"}, xhr=True
        )
        response2 = self.client.post(
            reverse("store_basket:basket_add"), {"productid": 3, "productqty": 1, "action": "post"}, xhr=True
        )
        self.assertEquals(response1.json(), {"qty": 5})
        # note:that the basket qty get updated after response1
        self.assertEquals(response2.json(), {"qty": 6})

    def test_basket_delete(self):
        """
        check the deletion functionality
        """

        # note the only session data still there is the one in the setup function
        response = self.client.post(
            reverse("store_basket:basket_delete"), {"productid": 2, "action": "post"}, xhr=True
        )
        shipping = Decimal(11.50)
        # add the shiping to the 24.00 subtotal
        self.assertEquals(response.json(), {"qty": 2, "subtotal": "35.50"})

    def test_basket_update(self):
        """
        test basket update functionality
        """
        response = self.client.post(
            reverse("store_basket:basket_update"), {"productid": 1, "productqty": 4, "action": "post"}, xhr=True
        )
        # add the shiping to the 24.00 total (we changed the name from subtotal to total in the ajax)
        self.assertEquals(response.json(), {"qty": 8, "total": "135.50", "item_total": 48})
