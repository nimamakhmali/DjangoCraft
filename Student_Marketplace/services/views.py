from django.http import JsonResponse


def list_services(_request):
    return JsonResponse({"services": []})
