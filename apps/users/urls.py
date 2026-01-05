from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views.register import UserRegistrationView
from apps.users.views.search import UserSearchView
from apps.users.views.login import UserLoginView
from apps.users.views.profile import UserProfileView
from apps.users.views.logout import LogoutView
from apps.users.views.admin_dashboard import AdminDashboardView
from apps.users.views.oauth_github import GitHubOAuthLoginView
from apps.users.views.oauth_github_callback import GitHubOAuthCallbackView
from apps.users.views.oauth_google import GoogleOAuthLoginView
from apps.users.views.oauth_google_callback import GoogleOAuthCallbackView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("search/", UserSearchView.as_view(), name="user-search"),
    # path("login/", UserLoginView.as_view(), name="user-login"),
    path("auth/login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="user-logout"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),

    # Admin-only API
    path("admin/dashboard/", AdminDashboardView.as_view(), name="admin-dashboard"),
    path("oauth/github/", GitHubOAuthLoginView.as_view(), name="github-oauth"),
    path(
        "oauth/github/callback/",
        GitHubOAuthCallbackView.as_view(),
        name="github-oauth-callback",
    ),
    path("oauth/google/", GoogleOAuthLoginView.as_view(), name="google-oauth"),
    path(
        "oauth/google/callback/",
        GoogleOAuthCallbackView.as_view(),
        name="google-oauth-callback",
    ),
    
]
