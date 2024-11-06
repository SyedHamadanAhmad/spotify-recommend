from django.http import JsonResponse

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define the paths to exclude from authorization checks
        self.excluded_paths = ['/', '/login', '/signup']  # Add more paths if needed

    def __call__(self, request):
        print(f"Request URL: {request.path}")
        
        # Check if the current path is in the excluded paths
        if request.path in self.excluded_paths:
            return self.get_response(request)  # Skip authorization check

        # Continue with authorization check if not in excluded paths
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Authorization header missing"}, status=403)

        # Proceed with the request if Authorization header exists
        response = self.get_response(request)
        return response
