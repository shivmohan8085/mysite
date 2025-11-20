from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='foodapp:get_all_data'), name='logout'),
    path("logout/", views.logout_user, name="logout"),
]
