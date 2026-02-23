from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import default_storage
from .managers import ItemManager
import os

class Item(models.Model):
    user_name= models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    item_name= models.CharField(max_length=30, db_index=True)
    item_desc= models.CharField(max_length=200)
    item_price=models.DecimalField(max_digits=6, decimal_places=2)
    # item_image=models.URLField(max_length=500, default='https://www.foodservicerewards.com/cdn/shop/t/262/assets/fsr-placeholder.png?v=45093109498714503231652397781')

    item_image = models.ImageField(
        upload_to="item_images/",
        default="default/default_dish.png",
        blank=True
    )
    is_available=models.BooleanField(default=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    is_deleted=models.BooleanField(default=False)
    deleted_at=models.DateTimeField(blank=True, null=True)



    @property
    def image_url(self):
        """
        Returns uploaded image if exists physically,
        otherwise returns default image.
        """
        if self.item_image:
            try:
                if os.path.exists(self.item_image.path):
                    return self.item_image.url
            except Exception:
                pass

        return settings.MEDIA_URL + "default/default_dish.png"




    # def delete(self, using=None, keep_parents=False):
    #     self.is_deleted = True
    #     self.deleted_at = timezone.now()
    #     self.save()


     # ---------------- SOFT DELETE ----------------
    def delete(self, using=None, keep_parents=False):

        # 🛑 Default image delete na ho
        if  self.item_image and self.item_image.name != "default/default_dish.png":
            # if default_storage.exists(self.item_image.name):
            #     default_storage.delete(self.item_image.name)

            image_path = os.path.join(settings.MEDIA_ROOT, self.item_image.name)
            if os.path.isfile(image_path):
                os.remove(image_path)


        # Soft delete logic
        self.is_deleted = True
        self.is_available = False
        self.deleted_at = timezone.now()
        self.save()

    # ---------------- SAFE IMAGE DISPLAY ----------------
    @property
    def image_url(self):
        """
        Returns uploaded image if exists physically,
        otherwise returns default image.
        """
        if self.item_image:
            try:
                if os.path.exists(self.item_image.path):
                    return self.item_image.url
            except Exception:
                pass

        return settings.MEDIA_URL + "default/default_dish.png"

    # ---------------- META ----------------
    class Meta:
        indexes = [
            models.Index(fields=["item_name", "item_price"])
        ]

    def __str__(self):
        return self.item_name

    objects = ItemManager()
    all_objects = models.Manager()