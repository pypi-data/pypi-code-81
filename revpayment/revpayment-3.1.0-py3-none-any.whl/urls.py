from django.urls import path
from rest_framework import routers

from revpayment.logistics.views import CVSCallback, LogisticCallBack, SelectCVS

from .views import (AddItemView, CallbackView, CartView, CartViewSet,
                    CheckoutView, ClearCartView, CreditView, DeleteItemView,
                    EditConfigView, EditItemView)

router = routers.DefaultRouter(trailing_slash=False)
router.register("cart", CartViewSet, basename="cart")
cart_urls = router.urls

checkout_urlpatterns = [
    path("checkout", CheckoutView.as_view(), name="payment-checkout"),
    path("callback", CallbackView.as_view(), name="payment-callback"),
    path("credit", CreditView.as_view(), name="payment-credit"),
    path("logistics/callback", LogisticCallBack.as_view(), name="logistic-callback"),
    path("logistics/cvs/select", SelectCVS.as_view(), name="logistic-cvs-select"),
    path("logistics/cvs/callback", CVSCallback.as_view(), name="logistic-cvs-callback"),
]

cart_urlpatterns = [
    path("", CartView.as_view(), name="cart-get"),
    path("clear", ClearCartView.as_view(), name="cart-clear"),
    path("item/add", AddItemView.as_view(), name="cart-add-item"),
    path("item/edit", EditItemView.as_view(), name="cart-edit-item"),
    path("item/delete", DeleteItemView.as_view(), name="cart-delete-item"),
    path("config/edit", EditConfigView.as_view(), name="cart-edit-config"),
]
