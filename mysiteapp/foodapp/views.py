from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.core.cache import caches
from django.views.decorators.cache import never_cache
from .models import Item
from .forms import ItemForm
import logging


food_cache = caches["foodapp_cache"]

# ✅ Logger setup
logger = logging.getLogger(__name__)


# ---------------- HOME ----------------
@login_required(login_url="users:login")
@never_cache   # ⭐ browser cache disable
@cache_page(60, cache="foodapp_cache") # cache for 60 seconds
def home(request):
    logger.info(f"Home page accessed by {request.user}")
    return render(request, "foodapp/home.html")


# ---------------- LIST VIEW ----------------
@login_required(login_url="users:login")
@never_cache   # ⭐ browser cache disable
@cache_page(60, cache="foodapp_cache") # cache for 60 seconds
def item_list(request):

    logger.info("Fetching item list")

    items = Item.objects.all().order_by("-updated_at", "-created_at")

    paginator = Paginator(items, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "item_list": page_obj,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
    }

    return render(request, "foodapp/display-data.html", context)


# ---------------- DETAIL VIEW ----------------
@login_required(login_url="users:login")
@never_cache   # ⭐ browser cache disable
@cache_page(60, cache="foodapp_cache") # cache for 60 seconds
def detail(request, id):

    logger.info(f"Fetching detail for item id: {id}")

    item = get_object_or_404(Item, pk=id)

    context = {
        "item_detail": item
    }
    return render(request, "foodapp/details.html", context)


# ---------------- CREATE VIEW ----------------
@login_required(login_url="users:login")
def create_item(request):

    if request.method == "POST":
        form = ItemForm(request.POST)

        if form.is_valid():
            item = form.save(commit=False)
            item.user_name = request.user
            item.save()

            # ✅ Clear cache after write
            food_cache.clear()

            logger.info(f"Item created by {request.user} | ID: {item.id}")

            return redirect("foodapp:get_all_data")

        else:
            logger.warning("Invalid form submission while creating item")

    else:
        form = ItemForm()

    return render(request, "foodapp/item-form.html", {"form": form})


# ---------------- UPDATE VIEW ----------------
@login_required(login_url="users:login")
def update_item(request, id):

    item = get_object_or_404(Item, pk=id)

    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)

        if form.is_valid():
            form.save()

            # ✅ Clear cache
            food_cache.clear()

            logger.info(f"Item updated | ID: {item.id}")

            return redirect("foodapp:get_all_data")

        else:
            logger.warning(f"Invalid update attempt for item id: {id}")

    else:
        form = ItemForm(instance=item)

    return render(
        request,
        "foodapp/item-form.html",
        {"form": form, "item": item}
    )


# ---------------- DELETE VIEW ----------------
@login_required(login_url="users:login")
def delete_item(request, id):

    item = get_object_or_404(Item, pk=id)
    item_id = item.id
    item.delete()

    # ✅ Clear cache
    food_cache.clear()

    logger.warning(f"Item deleted | ID: {item_id}")

    return redirect("foodapp:get_all_data")
