from django.urls import path
from .views import orders_add

app_name='orders'

urlpatterns = [
    path('add/',orders_add,name='add'),
]