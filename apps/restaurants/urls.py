'''
from django.urls import path
from apps.restaurants.views.menu import AddMenuItemView

from apps.restaurants.views.restaurants import (
    RestaurantListView,
    RestaurantCreateView,
)
from apps.restaurants.views.menu import (
    MenuCategoryCreateView,
    MenuItemCreateView,
    ToggleMenuItemAvailabilityView,
)


urlpatterns = [
    # Restaurant admin-only API
    path("menu/add/", AddMenuItemView.as_view(), name="add-menu-item"),
    path("", RestaurantListView.as_view(), name="restaurant-list"),
    path("create/", RestaurantCreateView.as_view(), name="restaurant-create"),

    path("menu/category/add/", MenuCategoryCreateView.as_view(), name="menu-category-add"),
    path("menu/item/add/", MenuItemCreateView.as_view(), name="menu-item-add"),
    path(
        "menu/item/<uuid:item_id>/toggle/",
        ToggleMenuItemAvailabilityView.as_view(),
        name="menu-item-toggle",
    ),
]
'''

from django.urls import path
from .views.restaurants import *
from .views.search_restaurants import RestaurantSearchView
from .views.menu_categories import *
from .views.menu_items import *
from .views.search_items import FoodItemSearchView
from .views.filter_by_category import MenuItemsByCategoryView
from .views.sorted_items import SortedMenuItemsView

urlpatterns = [

    # Restaurants
    path("", RestaurantListView.as_view()),
    path("create/", RestaurantCreateView.as_view()),
    path("<uuid:id>/", RestaurantDetailView.as_view()),
    path("<uuid:id>/update/", RestaurantUpdateView.as_view()),
    path("<uuid:id>/delete/", RestaurantDeleteView.as_view()),
    path("search/", RestaurantSearchView.as_view()),

    # Menu Categories
    path("menu/categories/", MenuCategoryListView.as_view()),
    path("menu/category/create/", MenuCategoryCreateView.as_view()),
    path("menu/category/<uuid:id>/update/", MenuCategoryUpdateView.as_view()),
    path("menu/category/<uuid:id>/delete/", MenuCategoryDeleteView.as_view()),

    # Menu Items
    path("menu/items/", MenuItemListView.as_view()),
    path("menu/item/create/", MenuItemCreateView.as_view()),
    path("menu/item/<uuid:id>/update/", MenuItemUpdateView.as_view()),
    path("menu/item/<uuid:id>/delete/", MenuItemDeleteView.as_view()),
    path("search/items/", FoodItemSearchView.as_view()),

    path(
        "browse/categories/<uuid:category_id>/items/",
        MenuItemsByCategoryView.as_view(),
        name="menu-items-by-category",
    ),

    path(
        "browse/categories/<uuid:category_id>/items/sorted/",
        SortedMenuItemsView.as_view(),
        name="sorted-menu-items",
    ),
]
