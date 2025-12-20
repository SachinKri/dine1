from django.urls import path
from apps.restaurants.views.menu import AddMenuItemView

urlpatterns = [
    # Restaurant admin-only API
    path("menu/add/", AddMenuItemView.as_view(), name="add-menu-item"),
]
