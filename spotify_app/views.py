# example/views.py
import requests
from django.conf import settings
from django.shortcuts import redirect, render
import urllib.parse
from django.http import HttpResponse, JsonResponse
from spotify_app.utils import Track
import json
from django.views.decorators.csrf import csrf_exempt

def spotify_login(request):
    client_id = settings.SPOTIFY_CLIENT_ID
    redirect_uri = urllib.parse.quote("http://127.0.0.1:8000/callback/")
    scope = (
    "user-read-private "
    "user-read-email "
    "playlist-modify-public "
    "playlist-modify-private "
    "user-library-read "
    "user-top-read "
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-read-currently-playing"
)
    auth_url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"

    return redirect(auth_url)

def spotify_callback(request):
    # Get the authorization code from the callback URL parameters
    code = request.GET.get("code")

    if not code:
        return JsonResponse({"error": "Authorization code not found"}, status=400)

    # Define token request parameters
    token_url = "https://accounts.spotify.com/api/token"
    redirect_uri = "http://127.0.0.1:8000/callback/"
    client_id = settings.SPOTIFY_CLIENT_ID
    client_secret = settings.SPOTIFY_CLIENT_SECRET

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    # Request an access token from Spotify
    response = requests.post(token_url, data=payload)
    response_data = response.json()

    if "access_token" in response_data:
        access_token = response_data["access_token"]
        refresh_token = response_data["refresh_token"]

        # Optionally save the tokens in the session or database for future use
        request.session["access_token"] = access_token
        request.session["refresh_token"] = refresh_token
        session_data = request.session.items()  # Get all items in the session
        session_str = "\n".join([f"{key}: {value}" for key, value in session_data])
        print(session_str)

        # Redirect to a success page or another view in your app
        return redirect("home")

    else:
        # Handle errors, such as if the access token request failed
        return JsonResponse({"error": "Failed to retrieve access token"}, status=400)

def reauthenticate(request):
    refresh_token=request.session["refresh_token"]
    if refresh_token:
        token_url = 'https://accounts.spotify.com/api/token'
        data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    }
        response=requests.post(token_url, data=data)
        if response.status_code==200:
            tokens=response.json()
            request.session['access_token']=tokens['access_token']
            print(request.session['access_token'])
            if 'refresh_token' in tokens:
                request.session['refresh_token'] = tokens['refresh_token']
            return JsonResponse({"status": "success", "message": "Reauthentication successful"}, safe=False)
        else:
            return JsonResponse("Failed to re-authenticate")
    else:
        return redirect("spotify_login")

def search_track(request):
    if request.session['access_token']:
        track_name=request.GET.get('track_name')
        access_token=request.session['access_token']
        if not track_name:
            return JsonResponse("Invalid Track Name", safe=False)
        url = "https://api.spotify.com/v1/search"
        headers = {
            "Authorization": f"Bearer {access_token}"
            }
        params = {
            "q": track_name,
            "type": "track",
            "limit": 5
            }

        # Make request to Spotify API
        response = requests.get(url, headers=headers, params=params)

        # Handle response
        if response.status_code == 200:
            return JsonResponse(response.json(), safe=False)
        else:
            return JsonResponse({"error": "Failed to fetch track data", "status_code": response.status_code}, status=response.status_code, safe=False)
    else:
        return redirect("reauthenticate")

@csrf_exempt
def get_several_features(request):
    if request.method!='POST':
        return JsonResponse("Invalid Request", status=405, safe=False)
    access_token=request.session['access_token']
    print(access_token)
    if not access_token:
        return redirect('reauthenticate')
    try:
        data=json.loads(request.body)
        track_ids=data.get("track_ids")
    except json.JSONDecodeError:
        return JsonResponse("Error parsing payload: track_ids not parsed", status=405, safe=False)
    if not track_ids:
        return JsonResponse({"error": "Missing track_ids in the request."}, status=400, safe=False)
    
    spotify_url="https://api.spotify.com/v1/audio-features"
    headers={
        'Authorization':f"Bearer {access_token}"
    }
    params={
        "ids": track_ids
    }

    response=requests.get(spotify_url, headers=headers, params=params)
    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch data from Spotify API."}, status=response.status_code, safe=False)
    print(response.json())
    return JsonResponse(response.json(), safe=False)




def index(request):
    access_token=request.session['access_token']
    if not access_token:
        return JsonResponse("No Token", safe=False)
    return render(request, 'post_req.html', {'access_token': access_token})