from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'page': self.get_page_number(request=self.request, paginator=self.page.paginator),
            'per_page':self.get_page_size(request=self.request),
            'total':len(data),
            'total_pages':0,
            'data':data

        })
