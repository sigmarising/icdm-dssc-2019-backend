from django.http import JsonResponse
from . import service


def article_list_map(request):
    return JsonResponse({"hello": "hello"})
