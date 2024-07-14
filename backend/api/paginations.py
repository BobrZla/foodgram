from rest_framework.pagination import PageNumberPagination

from .constant import PAGE_SIZE_PAGINATOR


class CustomPagination(PageNumberPagination):
    page_size = PAGE_SIZE_PAGINATOR
    page_size_query_param = "limit"
