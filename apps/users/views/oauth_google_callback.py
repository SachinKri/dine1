import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User
import os

class GoogleOAuthCallbackView(APIView):
    """
    OAuth callback → verify user → issue JWT
    """
    permission_classes = []

    def get(self, request):
        code = request.GET.get("code")

        if not code:
            return Response(
                {"error": "Authorization code not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Step 1: Exchange code for Google access token
        token_response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id":os.getenv("GOOGLE_CLIENT_ID") ,# settings.GOOGLE_CLIENT_ID,
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),# settings.GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI")# settings.GOOGLE_REDIRECT_URI,
            },
        )

        token_data = token_response.json()

        if "access_token" not in token_data:
            return Response(
                {"error": "Failed to obtain access token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Step 2: Fetch user profile from Google
        user_info_response = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={
                "Authorization": f"Bearer {token_data['access_token']}"
            },
        )

        user_info = user_info_response.json()
        email = user_info.get("email")
        name = user_info.get("name")

        if not email:
            return Response(
                {"error": "Email not provided by Google"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Step 3: Create or get local user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "full_name": name,
                "role": "customer",
                "is_active": True,
            },
        )

        # Step 4: Issue DineStream JWT
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                },
            },
            status=status.HTTP_200_OK,
        )