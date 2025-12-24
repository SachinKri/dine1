from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for exposing user data safely via APIs.
    Used in:
    - Login response
    - Profile API
    - Admin / internal services
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "role",
            "is_active",
            "created_at",
        )
        read_only_fields = (
            "id",
            "email",
            "role",
            "created_at",
        )
