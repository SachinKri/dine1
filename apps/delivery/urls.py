from django.urls import path
from apps.delivery.views.assignments import DeliveryAssignmentView

urlpatterns = [
    # Delivery partner-only API
    path("assignments/", DeliveryAssignmentView.as_view(), name="delivery-assignments"),
]
