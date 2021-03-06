from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class PageNumberPaginationDataOnly(PageNumberPagination):
    # Set any other options you want here like page_size

    def get_paginated_response(self, data):
        return Response(data)
