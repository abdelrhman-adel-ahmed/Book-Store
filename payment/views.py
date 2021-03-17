import json
import os

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from orders.views import payment_confirmation
from store_basket.store_basket import Basket

"""
1- payment_home: view (to create payment intent)
2- stripe_webhook: (to check wather the payment succeded or not)
3- order_placed: (view that user get redirect to after the payment succeded and clear the basket)
"""


@login_required
def payment_home(request):
    basket = Basket(request)
    # the intent amount sent to stripe must be in int foramte 12.99 we need to get tide of the . and send 1099 ,
    # so we change from dec to str
    total_price = str(basket.get_total_price())
    total_price = total_price.replace(".", "")
    total_price = int(total_price)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # intent is created when we enter the payment page
    intent = stripe.PaymentIntent.create(
        amount=total_price,
        currency="gbp",
        # send the user id to the stripe and when the uer complete the payment i will get this metadata back and match that
        # user with the order to know who actually paied wich order
        metadata={"userid": request.user.id},
    )
    context = {
        "client_secret": intent.client_secret,
        "STRIPE_PUBLISHABLE_KEY": os.environ.get("STRIPE_PUBLISHABLE_KEY"),
    }
    return render(request, "payment/payment_form.html", context)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None
    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == "payment_intent.succeeded":
        # send the order_key wich is the client_secret to the payment_confirmation function to update billing status to true
        payment_confirmation(event.data.object.client_secret)

    else:
        print("Unhandled event type {}".format(event.type))

    return HttpResponse(status=200)


def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "payment/orderplaced.html")
