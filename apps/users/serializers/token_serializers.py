from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer that embeds role and other claims
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # REQUIRED claims for downstream services
        token["user_id"] = str(user.id)
        token["role"] = user.role
        token["email"] = user.email

        return token
