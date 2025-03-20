from django.http import JsonResponse


def hosts(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


def port(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


def net(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


def asn(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


def app(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


def component(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


def loc(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


def org(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


def domain(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


def os(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


def soft(request):
    return JsonResponse({'data': {'q': request.GET['search']}})


def service(request):
    return JsonResponse({'data': {'q': request.GET['search']}})