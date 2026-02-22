from rest_framework import serializers
from .models import Item
from django.contrib.auth.models import User
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ItemSerializer(serializers.ModelSerializer):

    user_name = UserSerializer(read_only=True)  # for shoe user_name in api response

    class Meta:
        model = Item
        fields = [
            "id",
            "user_name",
            "item_name",
            "item_desc",
            "item_price",
            "item_image",
            "is_available",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user_name", "created_at", "updated_at"]

    # ✅ Item Name Validation
    def validate_item_name(self, value):
        if not re.match(r'^[A-Za-z]+(?: [A-Za-z]+)*$', value):
            raise serializers.ValidationError(
                "Item name should contain only letters and single spaces."
            )
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Item name must be at least 3 characters long."
            )
        return value.strip().title()

    # ✅ Price Validation
    def validate_item_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )
        if value > 999999:
            raise serializers.ValidationError(
                "Price is too large."
            )
        return value


    # ✅ Object-level validation
    def validate(self, data):
        item_name = data.get("item_name")
        item_desc = data.get("item_desc")

        if item_name and item_desc:
            if item_name.strip().lower() == item_desc.strip().lower():
                raise serializers.ValidationError(
                    "Item name and description cannot be the same."
                )

        return data