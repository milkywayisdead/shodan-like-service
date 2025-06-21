from django.shortcuts import render
from django.http import JsonResponse

from content import models


_DEFAULT_N = 4


CONTENT_PREVIEW_FUNCS = {
    '': lambda x: [],
    'news': models.NewsArticle.get_last_n,
    'filters': models.Filter.get_last_n,
    'functionality': models.Functionality.get_last_n,
}


CONTENT_ITEM_FUNCS = {
    'news': models.NewsArticle.get,
    'filters': models.Filter.get,
    'functionality': models.Functionality.get,
}


def get_content(request):
    content_type = request.GET.get('type', '')
    n = request.GET.get('n', _DEFAULT_N)
    func = CONTENT_PREVIEW_FUNCS[content_type]
    return JsonResponse({'data': func(int(n))})


def get_content_item(request):
    content_type = request.GET.get('type', '')
    item_id = request.GET.get('id', '')
    func = CONTENT_ITEM_FUNCS[content_type]
    return JsonResponse({
        'data': func(item_id)
    })
