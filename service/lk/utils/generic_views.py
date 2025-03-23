from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse

from .decorators import check_auth
from lk.db import db


PAGES_LIMIT = 20


class GenericSearchView(View):
    """
    Для поиска asn, hosts.
    Не требует авторизации.
    """
    search_type = ''

    def get(self, request, *args, **kwargs):
        term = request.GET['search']
        _ = self.search_type
        resp = {
            'hosts': db.generic_hosts(_, term),
            'hosts_total': db.generic_hosts_total(_, term),
            'ports': db.generic_ports(_, term),
            'tops': db.generic_tops(_, term),
        }
        return JsonResponse(resp)


class GenericSearchWithAuth(GenericSearchView):
    """
    Для поиска loc, org, app, soft, service, component, os.
    Есть проверка на авторизацию.
    """
    @method_decorator(check_auth)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class GenericPageView(View):
    """
    Для запросов хостов для пагинации.
    Не требует авторизации.
    """
    search_type = ''

    def get(self, request, *args, **kwargs):
        term = request.GET['search']
        _ = self.search_type
        page = self.get_page(request)
        hosts = db.generic_hosts(_, term, page=page)
        return JsonResponse({'hosts': hosts})

    def get_page(self, request):
        page = int(request.GET.get('page', 1))
        if request.user.is_authenticated:
            if page > PAGES_LIMIT:
                return PAGES_LIMIT
            return page
        return 1


class GenericPageWithAuth(GenericPageView):
    """
    Для запросов хостов для пагинации.
    Есть проверка на авторизацию.
    """
    @method_decorator(check_auth)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)