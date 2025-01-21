from django.shortcuts import render
import requests
from users import models
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

CLIENT_ID = "u-s4t2ud-1608c925fd96235cfd1e248ef9e1d02080614088dff0919ffcfd9fdda1b42328"
CLIENT_SECRET = "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"

def FortyTwoLogin(request):
    
    code = request.GET.get("code")
    
    print(code)
    
    if not code:
        return render(request, "login.html")
    
    token_url = "https://api.intra.42.fr/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": "http://localhost:8443/auth/42/login/",
    }
    
    response = requests.post(token_url, data=data)
    
    print(response)
    if response.status_code != 200:
        return render(request, "login.html")
    
    access_token = response.json().get("access_token")
    
    user_info_url = "https://api.intra.42.fr/v2/me/"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    user_response = requests.get(user_info_url, headers=headers)
    
    if user_response != 200:
        return JsonResponse({"error": "Failed to get user info"}, status=500)
    
    user_data = user_response.json()
    
    email = user_data.get("email")
    username = user_data.get("login")
    oauth_id = user_data.get("id")
    name = user_data.get("displayname")
    
    
    
    user, created = models.UserPong.objects.get_or_create(
        oauth_id=oauth_id,
        defaults={
            "email": email,
            "username": username,
            "name": name,
        }
    )
    
    if created:
        user.auth_method = "oauth"
        user.save()
    
    access_token = RefreshToken.for_user(user).access_token
    
    
    
    return JsonResponse({"access_token": str(access_token)}, status=200)
