from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Item
from .forms import ItemForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, TemplateView, CreateView , UpdateView , DeleteView
from django.urls import reverse_lazy


# @login_required(login_url="users:login")
# def home(request):
#     return render(request, "foodapp/home.html")

@method_decorator(login_required(login_url="users:login"), name='dispatch')
class HomeView(TemplateView):
    template_name = "foodapp/home.html"


#----------------------------------


# def item_list(request):
#     item_list = Item.objects.all()
#     context= {
#         'item_list':item_list
#     }
#     return render(request, "foodapp/display-data.html", context)

# @login_required(login_url="users:login")
# def item_list(request):
#     """Display all items"""
#     item_list = Item.objects.all()
#     return render(request, "foodapp/display-data.html", {"item_list": item_list})

@method_decorator(login_required(login_url="users:login"), name='dispatch')
class FoodItemListView(ListView):
    model = Item
    template_name = "foodapp/display-data.html"
    context_object_name= "item_list"      # by default ->  Item.objects.all()



#----------------------

# def detail(request, id):
#     item_detail = Item.objects.get(id=id)
#     context= {
#         'item_detail':item_detail
#     }
#     return render(request, "foodapp/details.html", context)

# @login_required(login_url="users:login")
# def detail(request, id):
#     """Display a specific item's details"""
#     item_detail = get_object_or_404(Item, id=id)
#     return render(request, "foodapp/details.html", {"item_detail": item_detail})


@method_decorator(login_required(login_url="users:login"), name='dispatch')
class FoodDetailView(DetailView):
    model= Item
    template_name = 'foodapp/details.html'
    context_object_name = 'item_detail'
    pk_url_kwarg = "id" 


#--------------------------------------------------





# @login_required(login_url="users:login")
# def create_item(request):
#     if request.method == 'POST':
#         form = ItemForm(request.POST)
#         if form.is_valid():
#             form.save()
#             print("Item created successfully")
#             return redirect('foodapp:get_all_data')
#     else:
#         form = ItemForm()

#     context = {
#         'form': form
#     }
#     return render(request, "foodapp/item-form.html", context)

@method_decorator(login_required(login_url="users:login"), name='dispatch')
class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm
    template_name = "foodapp/item-form.html"
    success_url = reverse_lazy("foodapp:get_all_data")

    def form_valid(self, form):
        form.instance.user_name= self.request.user
        print("Item created successfully")
        return super().form_valid(form)



#----------------------------------------------

# def update_item(request, id):
#     item_detail = Item.objects.get(id=id)
#     form = ItemForm(request.POST or None, instance=item_detail)
#     if form.is_valid():
#         form.save()
#         print("Item updated successfully")
#         return redirect('foodapp:get_all_data')
#     context = {
#         'form': form
#     }
#     return render(request, "foodapp/item-form.html", context)

# @login_required(login_url="users:login")
# def update_item(request, id):
#     """Update an existing item"""
#     item_detail = get_object_or_404(Item, id=id)

#     if request.method == 'POST':
#         form = ItemForm(request.POST, instance=item_detail)
#         if form.is_valid():
#             form.save()
#             print("Item updated successfully")
#             return redirect('foodapp:get_all_data')
#     else:
#         form = ItemForm(instance=item_detail)

#     return render(request, "foodapp/item-form.html", {"form": form})

@method_decorator(login_required(login_url="users:login"), name='dispatch')
class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm
    template_name = "foodapp/item-form.html"
    success_url = reverse_lazy("foodapp:get_all_data")
    context_object_name = "item"
    pk_url_kwarg = "id"   

    def form_valid(self, form):
        print("Item updated successfully")
        return super().form_valid(form)



#---------------


# def delete_item(request, id):
#     item = get_object_or_404(Item, id=id)
#     item.delete()
#     print("Item deleted successfully")
#     return redirect('foodapp:get_all_data')

# @login_required(login_url="users:login")
# def delete_item(request, id):
#     """Delete an item"""
#     item = get_object_or_404(Item, id=id)
#     item.delete()
#     print("Item deleted successfully")
#     return redirect('foodapp:get_all_data')


@method_decorator(login_required(login_url="users:login"), name='dispatch')
class ItemDeleteView(DeleteView):
    model = Item
    success_url = reverse_lazy("foodapp:get_all_data")
    pk_url_kwarg = "id"

    # Direct delete without confirmation template
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        print("Item deleted successfully")
        return redirect(self.success_url)
