from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse

from .decorators import check_auth, limit_check
from core.db import db
from .ratelimit import update_counter
from core.db.utils import get_ip


PAGES_LIMIT = 20


class GenericSearchView(View):
    """
    Для поиска asn, hosts.
    Не требует авторизации.
    """
    search_type = ''
    hosts_func = db.generic_hosts
    hosts_total_func = db.generic_hosts_total
    ports_func = db.generic_ports
    tops_func = db.generic_tops

    @method_decorator(limit_check)
    def get(self, request, *args, **kwargs):
        cls_ = self.__class__
        args_ = self.get_args(request)
        resp = {
            'hosts': cls_.hosts_func(*args_),
            'hosts_total': cls_.hosts_total_func(*args_),
            'ports': cls_.ports_func(*args_),
            'tops': cls_.tops_func(*args_),
        }

        # обновление счетчика запросов
        if request.user.is_authenticated:
            key, target = request.user.id, 'user'
        else:
            key, target = get_ip(request), 'ip'
        update_counter(key, target=target)

        return JsonResponse(resp)

    def get_args(self, request):
        return self.search_type, request.GET['search']


class GenericSearchWithAuth(GenericSearchView):
    """
    Для поиска loc, org, app, soft, service, component, os.
    Есть проверка на авторизацию.
    """
    @method_decorator(limit_check)
    @method_decorator(check_auth)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class GenericPageView(View):
    """
    Для запросов хостов для пагинации.
    Не требует авторизации.
    """
    search_type = ''
    search_func = db.generic_hosts

    @method_decorator(limit_check)
    def get(self, request, *args, **kwargs):
        args_ = self.get_args(request)
        page = self.get_page(request)
        hosts = self.__class__.search_func(page=page, *args_)

        # обновление счетчика запросов
        if request.user.is_authenticated:
            key, target = request.user.id, 'user'
        else:
            key, target = get_ip(request), 'ip'
        update_counter(key, target=target)

        return JsonResponse({'hosts': hosts})

    def get_args(self, request):
        return self.search_type, request.GET['search']

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
    @method_decorator(limit_check)
    @method_decorator(check_auth)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)