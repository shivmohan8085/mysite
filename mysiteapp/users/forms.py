from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile

# ✅ Registration Form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        help_texts = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Enter username"})
        self.fields["email"].widget.attrs.update({"placeholder": "Enter email"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Create password"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm password"})


# ✅ Profile Edit Form
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'location']
        help_texts = {
            "profile_image": "",
            "location": "",
        }

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.fields["profile_image"].widget.attrs.update({"placeholder": "Upload profile image"})
        self.fields["location"].widget.attrs.update({"placeholder": "Enter location"})


# ✅ Custom Password Change Form (No Help Texts)
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'placeholder': 'Enter current password'})
        self.fields['new_password1'].widget.attrs.update({'placeholder': 'Create new password'})
        self.fields['new_password2'].widget.attrs.update({'placeholder': 'Confirm new password'})

        # Remove help texts
        self.fields['new_password1'].help_text = ''
        self.fields['new_password2'].help_text = ''