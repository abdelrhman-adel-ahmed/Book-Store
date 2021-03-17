from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, reverse
from store.models import Product

from .store_basket import Basket


def basket_summary(request):
    basket = Basket(request)
    context = {"basket": basket}
    return render(request, "store_basket/summary.html", context)


def basket_add(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        product = get_object_or_404(Product, id=product_id)
        # function that add the current product to the session data
        basket.add(product, product_qty)
        # -----------------------------------------------------------------------
        # problem: add the last qty to the current selected qty ,
        # my fix: is to access the qty directlly not through the len function.
        # but if we have several items we need to use len so the problem still present----
        # final fix: use else condition on the add function in the context_processor to not create another
        # item in the dict and use str() to make the id string
        total_qty = basket.__len__()
        # -----------------------------------------------------------------------
        # total_qty=basket.session.get('skey')[product_id]['qty']
        response = JsonResponse({"qty": total_qty})
        return response

    # note: whene we refresh every thing get correct because session data get updated and the new values are placed


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_Id = int(request.POST.get("productid"))
        basket.delete(product_Id)
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({"qty": basketqty, "subtotal": baskettotal})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        product_Id = int(request.POST.get("productid"))
        product_Qty = int(request.POST.get("productqty"))
        basket.update(product_Id, product_Qty)
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        item_total = basket.get_item_total(product_Id)
        response = JsonResponse({"qty": basketqty, "total": baskettotal, "item_total": item_total})
        return response
