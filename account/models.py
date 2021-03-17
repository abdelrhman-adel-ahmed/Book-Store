import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    User,
)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, name, password, **other_fileds):
        other_fileds.setdefault("is_superuser", True)
        other_fileds.setdefault("is_staff", True)
        other_fileds.setdefault("is_active", True)

        if other_fileds.get("is_staff") is not True:
            raise ValueError("super user must be assigned is_staff=True ")

        if other_fileds.get("is_superuser") is not True:
            raise ValueError("super user must be assigend is_superuser=True")

        return self.create_user(email, name, password, **other_fileds)

    # override the create_user function that resposible for creating a user
    # see the doc https://docs.djangoproject.com/en/3.1/topics/auth/default/
    def create_user(self, email, name, password, **other_fileds):
        if not email:
            raise ValueError(_("you must provide an email"))
        # foo@bar.com and foo@BAR.com are equivalent; the domain part is case-insensitive according to the RFC specs.
        # Normalizing means providing a canonical representation, so that any two equivalent email strings normalize to
        # the same thing.
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fileds)
        # override the set_password function that resposible for setting the password for that user
        user.set_password(password)
        user.save()
        print(user.name)
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    mobile = models.CharField(max_length=20)
    # User Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ("-created",)

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            "l@1.com",
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.name


class Address(models.Model):
    """
    django automatically add primary key autoincreament id field when it create a table ,
    what we will gonna do is pass the id of the address through the url to django /account/address/1
    *so any one can change that and have access to the id form the url directly ,of course only the sign in
    user can do that to the range of id address he have
    *so uuid encode the id in a 128 bit number (32 hexadecimal characters and 4 hyphens). so it like that
    account/address/edite/123e4567-e89b-12d3-a456-426614174000 ,so its harder to hardwirte the id in the
    url bar for the users
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.CASCADE)
    full_name = models.CharField(_("Full Name"), max_length=150)
    phone = models.CharField(_("Phone Number"), max_length=50)
    postcode = models.CharField(_("Postcode"), max_length=50)
    address_line = models.CharField(_("Address Line 1"), max_length=255)
    address_line2 = models.CharField(_("Address Line 2"), max_length=255)
    town_city = models.CharField(_("Town/City/State"), max_length=150)
    delivery_instructions = models.CharField(_("Delivery Instructions"), max_length=255)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    default = models.BooleanField(_("Default"), default=False)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.customer.name}  address "
