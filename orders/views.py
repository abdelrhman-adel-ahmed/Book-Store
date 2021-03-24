from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from store_basket.store_basket import Basket

from .models import Order, OrderItem

"""
1- orders_add (view that called by the ajax call when user hit the pay button to check if any item price has been changed)
2- payment_confirmation (view that get invoked by stripe_webhook in payment app to if the payment succed to update
the billing_status to true)
"""


def orders_add(request):
    basket = Basket(request)
    # action that get sent along with the data in the ajax call to this url
    if request.POST.get("action") == "post":
        user_id = request.user.id
        order_key = request.POST.get("order_key")
        baskettotal = basket.get_total_price()
        print(basket.session)
        print(basket.basket)
        # check if the order is exist and only one order (because user may press pay and then go back before the payment actullay
        # finihsed and then go and press pay again)
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                user_id=user_id,
                full_name="name",
                address1="add1",
                address2="add2",
                total_paid=baskettotal,
                order_key=order_key,
            )
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(
                    order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"]
                )
        respone = JsonResponse({"sucess": "we are good"})
        return respone


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_order(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
