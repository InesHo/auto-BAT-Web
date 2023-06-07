from rest_framework import pagination

class StandardResultsSetPagination(pagination.PageNumberPagination):
    # modify the default pagination style
    page_size = 15 # set the page size to 15
    page_size_query_param = 'page_size'
    
