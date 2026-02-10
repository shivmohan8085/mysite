from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .managers import ItemManager


class Item(models.Model):
    user_name= models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    item_name= models.CharField(max_length=30, db_index=True)
    item_desc= models.CharField(max_length=200)
    item_price=models.DecimalField(max_digits=6, decimal_places=2)
    item_image=models.URLField(max_length=500, default='https://www.foodservicerewards.com/cdn/shop/t/262/assets/fsr-placeholder.png?v=45093109498714503231652397781')
    is_available=models.BooleanField(default=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    is_deleted=models.BooleanField(default=False)
    deleted_at=models.DateTimeField(blank=True, null=True)


    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


    class Meta:
        indexes= [
            models.Index(fields=["item_name","item_price"])
        ]

    def __str__(self):
        return self.item_name
    
    objects = ItemManager()
    all_objects = models.Manager()


class Category(models.Model):
    name = models.CharField(max_length=200)
    added_on= models.DateField(auto_now=True)

    def __str__(self):
        return self.name