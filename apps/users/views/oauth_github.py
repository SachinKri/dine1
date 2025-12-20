from urllib.parse import urlencode
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
import os


class GitHubOAuthLoginView(APIView):
    """
    Redirect user to GitHub OAuth consent screen
    """
    permission_classes = []

    def get(self, request):
        params = {
            "client_id": os.getenv("GITHUB_CLIENT_ID"), # settings.GITHUB_CLIENT_ID,
            "redirect_uri": os.getenv("GITHUB_REDIRECT_URI"), # settings.GITHUB_REDIRECT_URI,
            "scope": "read:user user:email",
        }

        github_auth_url = (
            "https://github.com/login/oauth/authorize?"
            + urlencode(params)
        )

        return redirect(github_auth_url)
