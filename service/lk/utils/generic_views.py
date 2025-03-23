from django.utils.decorators import method_decorator
from django.views import View

from .decorators import check_auth


class GenericSearchView(View):
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
    @method_decorator(check_auth)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class GenericPageView(View):
    search_type = ''

    def get(self, request, *args, **kwargs):
        term = request.GET['search']
        _ = self.search_type
        page = int(request.GET.get('page', 1))
        hosts = db.generic_hosts(_, term, page=page)
        return JsonResponse({'hosts': hosts})