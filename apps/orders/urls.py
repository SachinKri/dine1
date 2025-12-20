from django.urls import path
from apps.orders.views.place_order import PlaceOrderView

urlpatterns = [
    path("place/",PlaceOrderView.as_view(), name="place-order"),
]
