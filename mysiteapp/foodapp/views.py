from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Item
from .forms import ItemForm

from django.contrib.auth.decorators import login_required

@login_required(login_url="users:login")
def home(request):
    return render(request, "foodapp/home.html")




# def get_all_data(request):
#     item_list = Item.objects.all()
#     context= {
#         'item_list':item_list
#     }
#     return render(request, "foodapp/display-data.html", context)

@login_required(login_url="users:login")
def get_all_data(request):
    """Display all items"""
    item_list = Item.objects.all()
    return render(request, "foodapp/display-data.html", {"item_list": item_list})

# def detail(request, id):
#     item_detail = Item.objects.get(id=id)
#     context= {
#         'item_detail':item_detail
#     }
#     return render(request, "foodapp/details.html", context)

@login_required(login_url="users:login")
def detail(request, id):
    """Display a specific item's details"""
    item_detail = get_object_or_404(Item, id=id)
    return render(request, "foodapp/details.html", {"item_detail": item_detail})



@login_required(login_url="users:login")
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            print("Item created successfully")
            return redirect('foodapp:get_all_data')
    else:
        form = ItemForm()

    context = {
        'form': form
    }
    return render(request, "foodapp/item-form.html", context)



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

@login_required(login_url="users:login")
def update_item(request, id):
    """Update an existing item"""
    item_detail = get_object_or_404(Item, id=id)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item_detail)
        if form.is_valid():
            form.save()
            print("Item updated successfully")
            return redirect('foodapp:get_all_data')
    else:
        form = ItemForm(instance=item_detail)

    return render(request, "foodapp/item-form.html", {"form": form})


# def delete_item(request, id):
#     item = get_object_or_404(Item, id=id)
#     item.delete()
#     print("Item deleted successfully")
#     return redirect('foodapp:get_all_data')

@login_required(login_url="users:login")
def delete_item(request, id):
    """Delete an item"""
    item = get_object_or_404(Item, id=id)
    item.delete()
    print("Item deleted successfully")
    return redirect('foodapp:get_all_data')
