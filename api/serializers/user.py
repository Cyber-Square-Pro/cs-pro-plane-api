from rest_framework import serializers
from db.models import User
from rest_framework import serializers

class UserEmailSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ('email',)
        