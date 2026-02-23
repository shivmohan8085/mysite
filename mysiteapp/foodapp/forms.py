from django import forms
from .models import Item
from django.core.exceptions import ValidationError
import re


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_desc', 'item_price', 'item_image']

       
        # Optional: Add styling or placeholders
        widgets = {
            'item_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter item name'
            }),
            'item_desc': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description',
                'rows': 3
            }),
            'item_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price'
            }),
            # 'item_image': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Enter image URL'
            # }),

            'item_image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    # 🔥 1️⃣ Item Name Validation
    def clean_item_name(self):

        name = self.cleaned_data.get("item_name")

        if len(name) < 3:
            raise ValidationError(
                "Item name must be at least 3 characters long."
            )

        # Only letters + spaces allowed
        if not re.match(r'^[A-Za-z ]+$', name):
            raise ValidationError(
                "Item name should contain only letters and spaces."
            )

        return name.strip().title()  
        # trim + capitalize (professional touch)

    # 🔥 2️⃣ Description Validation
    def clean_item_desc(self):

        desc = self.cleaned_data.get("item_desc")

        if len(desc) < 10:
            raise ValidationError(
                "Description must be at least 10 characters."
            )

        return desc.strip()

    # 🔥 3️⃣ Price Validation
    def clean_item_price(self):

        price = self.cleaned_data.get("item_price")

        if price <= 0:
            raise ValidationError(
                "Price must be greater than zero."
            )

        if price > 100000:
            raise ValidationError(
                "Price seems unrealistic."
            )

        return price


    # 🔥 5️⃣ FORM LEVEL Validation (Senior Move)
    def clean(self):
        cleaned_data = super().clean()

        name = cleaned_data.get("item_name")
        desc = cleaned_data.get("item_desc")

        if name and desc:
            if name.strip().lower() == desc.strip().lower():
                raise ValidationError(
                    "Description cannot be exactly same as item name."
                )

        return cleaned_data