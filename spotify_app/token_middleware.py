from django.shortcuts import redirect
from django.urls import reverse

class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Define paths that should bypass the middleware checks
        excluded_paths = [
            reverse('spotify_login'),
            reverse('reauthenticate'),
            reverse('spotify_callback'),
            reverse('home')
        ]
        
        # Check if the current request path is not in the excluded paths
        if request.path not in excluded_paths:
            # Safely retrieve the tokens from the session, with default to None if not present
            access_token = request.session.get('access_token')
            refresh_token = request.session.get('refresh_token')
            
            # Redirect to appropriate view based on token presence
            if not access_token:
                # Redirect to reauthenticate if refresh_token exists
                if refresh_token:
                    return redirect(reverse('reauthenticate'))
                # Otherwise, redirect to login
                else:
                    return redirect(reverse('login'))
        
        # Proceed with the request if all checks are passed
        response = self.get_response(request)
        return response
