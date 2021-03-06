from django.urls import path
from . import controller as ctrl


urlpatterns = [
    path('articleListMap', ctrl.article_list_map),
    path('articleInfo', ctrl.article_info),
    path('knowledgeGraph', ctrl.knowledge_graph)
]
