from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

from .forms import PwdResetConfirmForm, PwdResetForm, UserLoginForm
from .views import (
    account_activate,
    account_dashboard,
    account_delete,
    account_edit,
    account_logout,
    account_register,
    add_address,
    add_to_wishlist,
    delete_address,
    edit_address,
    set_default,
    user_wishlist,
    view_address,
)

app_name = "account"

urlpatterns = [
    # register
    path("register/", account_register, name="register"),
    path("activate/<slug:uidb64>/<slug:token>", account_activate, name="activate"),
    # login,logout
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="account/login/login.html", form_class=UserLoginForm),
        name="login",
    ),
    path("logout/", account_logout, name="logout"),
    # reset password
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account/password_reset/password_reset.html",
            email_template_name="account/password_reset/password_reset_email.html",
            success_url=reverse_lazy("account:password_reset_done"),
            form_class=PwdResetForm,
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset-password-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password_reset/password_reset_confirm.html",
            success_url=reverse_lazy("account:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password_reset/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # password change
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            template_name="account/password_change/password_change.html",
            success_url=reverse_lazy("account:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password-change-done/",
        auth_views.PasswordChangeDoneView.as_view(template_name="account/password_change/password_change_done.html"),
        name="password_change_done",
    ),
    # user account
    path("dashboard/", account_dashboard, name="dashboard"),
    path("profile/edit", account_edit, name="profile-edit"),
    path("profile/delete", account_delete, name="delete_user"),
    path(
        "profile/delete_confirm",
        TemplateView.as_view(template_name="account/dashboard/delete_confrim.html"),
        name="delete_confirm",
    ),
    # address crud
    path("addresses/", view_address, name="addresses"),
    path("add_address/", add_address, name="add_address"),
    path("addresses/edit/<slug:id>/", edit_address, name="edit_address"),
    path("addresses/delete/<slug:id>/", delete_address, name="delete_address"),
    path("addresses/set_default/<slug:id>/", set_default, name="set_default"),
    # wishlist
    path("wishlist/add_to_wishlis/<slug:id>/", add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/", user_wishlist, name="user_wishlist"),
]
