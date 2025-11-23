from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    user_name= models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    item_name= models.CharField(max_length=30)
    item_desc= models.CharField(max_length=200)
    item_price=models.IntegerField()
    item_image=models.CharField(max_length=500, default='https://www.foodservicerewards.com/cdn/shop/t/262/assets/fsr-placeholder.png?v=45093109498714503231652397781')
    
    def __str__(self):
        return self.item_name

