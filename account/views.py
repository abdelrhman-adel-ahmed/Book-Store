from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from orders.views import user_order
from store.models import Product

from .forms import ProfileUpdate, RegistrationForm, UserAddressForm
from .models import Address, Customer
from .token import account_activation_token

"""
account app views:
1- account_register: if user doesnot have and account
2- account_activate: after user register email is been sent this view handle the activation of the user account
3- account_dashboard: the dashboard
4- account_logout: logout the user
5- account_delete: delete the user account by deactivate user account
"""
"""
1-# check the doc to see all fileds method and attribute of user model in django
 https://docs.djangoproject.com/en/3.1/ref/contrib/auth/
2-see the doc: https://docs.djangoproject.com/en/3.1/ref/contrib/sites/#django.contrib.sites.shortcuts.get_current_site
3- see the doc:https://docs.djangoproject.com/en/3.1/topics/templates/#django.template.loader.render_to_string
   render_to_string(template_name, context=None, request=None, using=None) --> part of  django.template.loader
4-see the doc: https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#attributes
  email_user(subject, message, from_email=None, **kwargs) --> part of User class

"""


def account_register(request):

    if request.user.is_authenticated:
        return redirect("account:dashboard")

    if request.method == "POST":
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data["email"]
            user.name = register_form.cleaned_data["name"]
            user.set_password(register_form.cleaned_data["password1"])
            # i dont want to activate user right away ,user will be activated after checking the email confirmation
            user.is_active = False
            user.save()
            # setup email
            current_site = get_current_site(request)
            subject = "Activate your account"
            context = {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            }
            message = render_to_string("account/registration/account_activation_email.html", context)
            user.email_user(subject=subject, message=message)
            return render(request, "account/registration/register_compelete.html")
    else:
        register_form = RegistrationForm()
    return render(request, "account/registration/register.html", {"form": register_form})


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:dashboard")
    else:
        return render(request, "account/registration/activation_invalid.html")


@login_required
def account_dashboard(request):
    # get the orders that user pay for
    orders = user_order(request)
    context = {"orders": orders}
    return render(request, "account/dashboard/dashboard.html", context)


def account_logout(request):
    logout(request)
    return redirect("/")


@login_required
def account_edit(request):
    if request.method == "POST":
        user_form = ProfileUpdate(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = ProfileUpdate(instance=request.user)

    context = {"user_form": user_form}
    return render(request, "account/dashboard/account_edit.html", context)


@login_required
def account_delete(request):
    user = Customer.objects.get(name=request.user)
    user.is_active = False
    user.save()
    return redirect("account:delete_confirm")


# Address
@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    context = {"addresses": addresses}
    return render(request, "account/address/addresses.html", context)


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        context = {"form": address_form}
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()
    context = {"form": address_form, "title": "Add Addresses"}
    return render(request, "account/address/add_address.html", context)


@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(id=id)
        address_form = UserAddressForm(data=request.POST, instance=address)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(id=id)
        address_form = UserAddressForm(instance=address)
    context = {"form": address_form, "title": "Edite Addresses"}
    return render(request, "account/address/add_address.html", context)


@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id).delete()
    return HttpResponseRedirect(reverse("account:addresses"))


@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(id=id).update(default=True)
    return HttpResponseRedirect(reverse("account:addresses"))


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    # check if the user aleady added the product to the wishlist
    if product.user_wishlist.filter(id=request.user.id).exists():
        product.user_wishlist.remove(request.user)
        messages.success(request, f"{product.title} has been removed from your wishlist")
    else:
        product.user_wishlist.add(request.user)
        messages.success(request, f"{product.title} added to your wishlist")

    for query in connection.queries:
        print(query)

    # referer header: url from which the current url loaded from
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def user_wishlist(request):
    # every product that is added to the wish list
    wishlist = Product.objects.filter(user_wishlist=request.user)
    context = {"wishlist": wishlist}
    return render(request, "account/dashboard/user_wishlist.html", context)
