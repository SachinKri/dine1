import os
from urllib.parse import urlencode
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView

class GoogleOAuthLoginView(APIView):
    """
    Redirect user to Google OAuth login
    """
    permission_classes = []

    def get(self, request):
        query_params = {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"), #settings.GOOGLE_CLIENT_ID,
            "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"), #settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent",
        }

        auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            + urlencode(query_params)
        )

        return redirect(auth_url)
