from django.http import JsonResponse

class EnsureJsonMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 403 and "text/html" in response['Content-Type']:
            return JsonResponse({'status': 'error', 'message': 'Forbidden'}, status=403)
        return response
