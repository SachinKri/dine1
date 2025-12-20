from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.permissions import IsAdminRole


class AdminDashboardView(APIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        return Response({
            "message": "Welcome to Admin Dashboard"
        })