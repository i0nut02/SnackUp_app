from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_views, name="login"),
    path("signup", views.signup_views, name="signup"),
    path("logout", views.logout_views, name="logout"),
    path("menu", views.menu, name="menu"),
    path("cart", views.cart, name="cart"),
    path("orders", views.orders, name="orders"),
    path("account", views.account, name="account"),
    path("change_information", views.change_information, name="change_information"),
    path("change_information/<str:change_info>/", views.change_information, name="change_information")
]