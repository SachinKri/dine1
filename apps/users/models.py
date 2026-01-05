from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager
import uuid

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("restaurant_admin", "Restaurant Admin"),
        ("delivery_partner", "Delivery Partner"),
        ("admin", "Admin"),
    )

    # id = models.BigAutoField(primary_key=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()   # IMPORTANT

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users_user"

    def __str__(self):
        return self.email


class Address(models.Model):
    # user_id = models.BigIntegerField()
    user_id = models.UUIDField(db_index=True)
    address_line = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, 
                                   decimal_places=6, 
                                   null=True,
                                   blank=True)
    longitude = models.DecimalField(max_digits=9, 
                                    decimal_places=6, 
                                    null=True,
                                    blank=True)
    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users_address"
        indexes = [
            models.Index(fields=["user_id"]),
            models.Index(fields=["user_id", "is_default"]),
            ]