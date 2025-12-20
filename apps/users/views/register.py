from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers.register import UserRegistrationSerializer


class UserRegistrationView(APIView):
    """
    User Registration API
    """

    permission_classes = []  # Public endpoint

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                    "created_at": user.created_at,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
