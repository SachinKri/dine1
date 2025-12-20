from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.permissions import IsCustomerRole


class PlaceOrderView(APIView):
    permission_classes = [IsCustomerRole]

    def post(self, request):
        return Response({
            "message": "Order placed successfully",
            "user": request.user.email
        })
