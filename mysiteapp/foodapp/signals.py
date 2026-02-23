import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Item


# 🗑️ DELETE IMAGE FILE WHEN OBJECT DELETED
@receiver(post_delete, sender=Item)
def delete_image_on_object_delete(sender, instance, **kwargs):
    if instance.item_image:
        if os.path.isfile(instance.item_image.path):
            os.remove(instance.item_image.path)


# 🔁 DELETE OLD IMAGE WHEN NEW IMAGE UPLOADED
@receiver(pre_save, sender=Item)
def delete_old_image_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Item.objects.get(pk=instance.pk).item_image
    except Item.DoesNotExist:
        return False

    new_file = instance.item_image

    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)