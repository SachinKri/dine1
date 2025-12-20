from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.permissions import IsDeliveryPartnerRole


class DeliveryAssignmentView(APIView):
    permission_classes = [IsDeliveryPartnerRole]

    def get(self, request):
        return Response({
            "message": "Assigned deliveries list"
        })
