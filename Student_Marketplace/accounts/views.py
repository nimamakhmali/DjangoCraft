from django.http import JsonResponse


def ping(_request):
    return JsonResponse({"accounts": "pong"})

# Create your views here.
