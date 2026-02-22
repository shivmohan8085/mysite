from rest_framework import serializers
from .models import Item
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ItemSerializer(serializers.ModelSerializer):
    
    # user_name = serializers.StringRelatedField()
    user_name = UserSerializer(read_only=True)

    class Meta:
        model = Item
        fields = "__all__"

