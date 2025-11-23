from django.urls import path
from . import views

app_name = 'foodapp'


urlpatterns = [
    # path("", views.home, name="home"),
    path("", views.HomeView.as_view(), name="home"),


    # path('all-items/', views.item_list, name='get_all_data'),
    path('all-items/', views.FoodItemListView.as_view(), name='get_all_data'),

    # path('items/<int:id>/', views.detail, name='detail'),
    path('items/<int:id>/', views.FoodDetailView.as_view(), name='detail'),

    # path('items/add/', views.create_item, name='create_item'),
    path('items/add/', views.ItemCreateView.as_view(), name='create_item'),

    # path('items/<int:id>/update/', views.update_item, name='update_item'),
    path('items/<int:id>/update/', views.ItemUpdateView.as_view(), name='update_item'),

    # path('items/<int:id>/delete/', views.delete_item, name='delete_item'),
    path('items/<int:id>/delete/', views.ItemDeleteView.as_view(), name='delete_item'),

]