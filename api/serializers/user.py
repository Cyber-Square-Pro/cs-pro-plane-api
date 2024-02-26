from rest_framework import serializers
from db.models import User
from .base import BaseSerializer
from rest_framework import serializers

class UserEmailSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ('email',)

class UserLiteSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "avatar",
            "is_bot",
            "display_name",
        ]
        read_only_fields = [
            "id",
            "is_bot",
        ]
