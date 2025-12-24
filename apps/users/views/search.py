from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from apps.users.models import User
from apps.users.serializers.users import UserSerializer


class UserSearchView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def get_queryset(self):
        q = self.request.query_params.get("q")

        if not q:
            return User.objects.none()

        return User.objects.filter(
            email__icontains=q
        )
