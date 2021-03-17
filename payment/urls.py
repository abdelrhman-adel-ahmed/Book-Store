from django.urls import path

from .views import payment_home,order_placed,stripe_webhook
app_name='payment'

urlpatterns=[
    path('',payment_home,name='payment_home'),
    path('orderplaced/',order_placed,name='order_placed'),
    path('webhook/',stripe_webhook,name='stripe_webhook'),
]