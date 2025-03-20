from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


def check_auth(view, *args, **kwargs):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 401}, status=401)
        return view(request, *args, **kwargs)
    return wrapper


def hosts(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


def port(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


def net(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


def asn(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


@check_auth
def app(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


@check_auth
def component(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


@check_auth
def loc(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


@check_auth
def org(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


@check_auth
def domain(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


@check_auth
def os(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


@check_auth
def soft(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


@check_auth
def service(request):
    return JsonResponse({'data': {'q': request.GET['search']}})