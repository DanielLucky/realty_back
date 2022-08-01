from rest_framework.pagination import PageNumberPagination


class PaginationRealtyList(PageNumberPagination):
    page_size = 5
    max_page_size = 1000
