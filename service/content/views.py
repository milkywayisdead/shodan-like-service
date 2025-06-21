from django.shortcuts import render
from django.http import JsonResponse

from content import models


_DEFAULT_N = 4


CONTENT_FUNCS = {
    '': lambda x: [],
    'news': models.NewsArticle.get_last_n,
    'filters': models.Filter.get_last_n,
    'functionality': models.Functionality.get_last_n,
}


def get_content(request):
    content_type = request.GET.get('type', '')
    func = CONTENT_FUNCS[content_type]
    return JsonResponse({'data': func(_DEFAULT_N)})
