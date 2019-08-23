from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.cache import cache_control, cache_page
from . import service


@cache_page(60 * 60 * 24)
def article_list_map(request):
    """
    ctrl for all article list
    :param request: request
    :return: category and id
    """
    if request.method != "GET":
        return HttpResponseBadRequest("This http method is not allowed!")
    else:
        return JsonResponse(service.service_article_list())


@cache_page(60 * 60 * 24)
def article_info(request):
    """
    ctrl for all article info
    :param request: request
    :return: content and graph
    """
    if request.method != "GET":
        return HttpResponseBadRequest("This http method is not allowed!")
    else:
        return JsonResponse(service.service_article_info(
            request.GET['category'],
            request.GET['identity'],
            request.GET['strength'],
            request.GET['categoryType']
        ))


@cache_page(60 * 5)
def knowledge_graph(request):
    """
    ctrl for text 2 knowledge graph
    :param request: request
    :return: json dict
    """
    if request.method != "GET":
        return HttpResponseBadRequest("This http method is not allowed!")
    else:
        return JsonResponse({
            "graph": service.service_knowledge_graph(
                request.GET["text"],
                request.GET['strength'],
                request.GET['category']
            )
        })
