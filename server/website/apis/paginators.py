from rest_framework.pagination import PageNumberPagination


class PageNumberPaginationMixin(PageNumberPagination):
    page_size_query_param = 'page_size'


class LargeResultsSetPagination(PageNumberPaginationMixin):
    page_size = 1000
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPaginationMixin):
    page_size = 100
    max_page_size = 1000
    
    
class MediumResultsSetPagination(PageNumberPaginationMixin):
    page_size = 50
    max_page_size = 500

    
class SmallResultsSetPagination(PageNumberPaginationMixin):
    page_size = 10
    max_page_size = 100


class TinyResultsSetPagination(PageNumberPaginationMixin):
    page_size = 1
    max_page_size = 50