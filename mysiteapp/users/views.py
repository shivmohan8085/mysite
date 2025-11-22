from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, ProfileEditForm, CustomPasswordChangeForm   # ✅ import custom form
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please login.")
            return redirect("users:login")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("users:login")


@login_required(login_url="users:login")
def user_profile(request):
    profile = request.user.profile

    # Default forms
    p_form = ProfileEditForm(instance=profile)
    pass_form = CustomPasswordChangeForm(request.user)   # ✅ use custom form

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            p_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
            if p_form.is_valid():
                p_form.save()
                messages.success(request, "Profile updated successfully ✅")
                return redirect('users:user_profile')

        elif 'change_password' in request.POST:
            pass_form = CustomPasswordChangeForm(request.user, request.POST)   # ✅ use custom form
            if pass_form.is_valid():
                user = pass_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully 🔒")
                return redirect('users:user_profile')

    return render(request, 'users/profile.html', {
        'p_form': p_form,
        'pass_form': pass_form,
    })