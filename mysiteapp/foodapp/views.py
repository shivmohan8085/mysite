from django.shortcuts import render
from django.http import HttpResponse
from .models import Item

def index(request):
    item_list = Item.objects.all()
    context= {
        'item_list':item_list
    }
    return render(request, "foodapp/index.html", context)

def detail(request, id):
    item_detail = Item.objects.get(id=id)
    context= {
        'item_detail':item_detail
    }
    return render(request, "foodapp/details.html", context)


