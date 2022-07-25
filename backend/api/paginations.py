from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class PagePagination(PageNumberPagination):
    page_size = settings.REST_FRAMEWORK['PAGE_SIZE_FOR_RECIPES']
    page_size_query_param = 'limit'
