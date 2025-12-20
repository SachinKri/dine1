from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers.login import UserLoginSerializer


class UserLoginView(APIView):
    """
    User Login API (JWT)
    """

    permission_classes = []  # Public endpoint

    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
