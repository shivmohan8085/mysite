# from django.contrib import admin
# from .models import Item

# admin.site.register(Item)
from django.contrib import admin
from .models import Item , Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["id", "item_name", "item_price", "is_deleted", "created_at"]
    list_filter = ["is_deleted"]

    def get_queryset(self, request):
        # IMPORTANT: custom manager ko bypass karne ke liye
        return Item.all_objects.all()


admin.site.register(Order)