import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User
import os


class GitHubOAuthCallbackView(APIView):
    """
    GitHub OAuth callback → verify user → issue JWT
    """
    permission_classes = []

    def get(self, request):
        code = request.GET.get("code")

        if not code:
            return Response(
                {"error": "Authorization code missing"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Step 1: Exchange code for GitHub access token
        token_response = requests.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": os.getenv("GITHUB_CLIENT_ID"), # settings.GITHUB_CLIENT_ID,
                "client_secret": os.getenv("GITHUB_CLIENT_SECRET"), # settings.GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": os.getenv("GITHUB_REDIRECT_URI") # settings.GITHUB_REDIRECT_URI,
            },
        )

        token_data = token_response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            return Response(
                {"error": "Failed to obtain access token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Step 2: Fetch GitHub user profile
        user_response = requests.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )
        user_data = user_response.json()

        # Step 3: Fetch primary email
        email_response = requests.get(
            "https://api.github.com/user/emails",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )
        emails = email_response.json()

        primary_email = next(
            (e["email"] for e in emails if e.get("primary")),
            None,
        )

        if not primary_email:
            return Response(
                {"error": "Email not available from GitHub"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Step 4: Create or map local user
        user, _ = User.objects.get_or_create(
            email=primary_email,
            defaults={
                "full_name": user_data.get("name")
                or user_data.get("login"),
                "role": "customer",
                "is_active": True,
            },
        )

        # Step 5: Issue DineStream JWT
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
