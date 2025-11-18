from django.urls import path
from . import views

app_name = 'foodapp'

urlpatterns = [
    path('', views.index, name='index'),          # Home page → index view
    path('items/<int:id>/', views.detail, name='detail'),  # Detail page
]