from rest_framework.pagination import PageNumberPagination


class FoodItemPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = None
    max_page_size = 3
