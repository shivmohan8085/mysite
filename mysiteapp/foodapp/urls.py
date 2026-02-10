from django.urls import path
from . import views

app_name = "foodapp"

urlpatterns = [
    path("", views.home, name="home"),
    path("all-items/", views.item_list, name="get_all_data"),
    path("items/<int:id>/", views.detail, name="detail"),
    path("items/add/", views.create_item, name="create_item"),
    path("items/<int:id>/update/", views.update_item, name="update_item"),
    path("items/<int:id>/delete/", views.delete_item, name="delete_item"),
]
