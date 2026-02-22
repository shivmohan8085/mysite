from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page, never_cache
from django.core.cache import caches
from .models import Item
from .forms import ItemForm
import logging


# Use named cache
food_cache = caches["foodapp_cache"]

# Use app-specific logger (IMPORTANT)
logger = logging.getLogger("foodapp")

# ---------------- HOME ----------------
@login_required(login_url="users:login")
@never_cache #  browser cache disable
@cache_page(60, cache="foodapp_cache")
def home(request):
    logger.info("HOME OPENED | user=%s", request.user)
    logger.debug("HOME REQUEST | method=%s | path=%s", request.method, request.path)

    return render(request, "foodapp/home.html")


# ---------------- LIST VIEW ----------------
@login_required(login_url="users:login")
@never_cache
@cache_page(60, cache="foodapp_cache")
def item_list(request):

    page = request.GET.get("page", 1)
    logger.info("ITEM LIST OPENED | user=%s | page=%s", request.user, page)
    logger.debug("Ordering items by updated_at, created_at")

    items = Item.objects.all().order_by("-updated_at", "-created_at")

    paginator = Paginator(items, 5)
    page_obj = paginator.get_page(page)

    logger.debug(
        "Pagination applied | current_page=%s | total_pages=%s",
        page_obj.number,
        page_obj.paginator.num_pages
    )

    context = {
        "item_list": page_obj,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
    }

    return render(request, "foodapp/display-data.html", context)


# ---------------- DETAIL VIEW ----------------
@login_required(login_url="users:login")
@never_cache
@cache_page(60, cache="foodapp_cache")
def detail(request, id):

    logger.info("ITEM DETAIL OPENED | user=%s | item_id=%s", request.user, id)

    try:
        item = get_object_or_404(Item, pk=id)
        logger.debug("Item fetched successfully | item_id=%s", id)

    except Exception as e:
        logger.error(
            "FAILED TO FETCH ITEM | item_id=%s | error=%s",
            id,
            e,
            exc_info=True
        )
        raise

    return render(request, "foodapp/details.html", {"item_detail": item})


# ---------------- CREATE VIEW ----------------
@login_required(login_url="users:login")
def create_item(request):

    logger.debug("CREATE ITEM VIEW OPENED | user=%s", request.user)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.user_name = request.user
            item.save()

            food_cache.clear()

            logger.info(
                "ITEM CREATED | item_id=%s | user=%s",
                item.id,
                request.user
            )

            return redirect("foodapp:get_all_data")

        else:
            logger.warning(
                "INVALID CREATE FORM | user=%s | errors=%s",
                request.user,
                form.errors
            )

    else:
        # ⭐ VERY IMPORTANT
        form = ItemForm()

    return render(request, "foodapp/item-form.html", {"form": form})


# ---------------- UPDATE VIEW ----------------
@login_required(login_url="users:login")
def update_item(request, id):

    logger.debug("UPDATE VIEW OPENED | user=%s | item_id=%s", request.user, id)

    item = get_object_or_404(Item, pk=id)

    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)

        if form.is_valid():
            form.save()

            food_cache.clear()

            logger.info(
                "ITEM UPDATED | item_id=%s | user=%s",
                id,
                request.user
            )
            logger.debug("Food cache cleared after update")

            return redirect("foodapp:get_all_data")

        else:
            logger.warning(
                "INVALID UPDATE FORM | item_id=%s | user=%s | errors=%s",
                id,
                request.user,
                form.errors
            )

    return render(
        request,
        "foodapp/item-form.html",
        {"form": ItemForm(instance=item), "item": item}
    )


# ---------------- DELETE VIEW ----------------
@login_required(login_url="users:login")
def delete_item(request, id):

    logger.warning(
        "DELETE ATTEMPT | user=%s | item_id=%s",
        request.user,
        id
    )

    try:
        item = get_object_or_404(Item, pk=id)
        item.delete()

        food_cache.clear()

        logger.warning(
            "ITEM DELETED | item_id=%s | user=%s",
            id,
            request.user
        )
        logger.debug("Food cache cleared after delete")

    except Exception as e:
        logger.critical(
            "DELETE FAILED | item_id=%s | user=%s | error=%s",
            id,
            request.user,
            e,
            exc_info=True
        )
        raise

    return redirect("foodapp:get_all_data")






# -------------------------------- using json response-----------------------------------------------

from django.http import JsonResponse

def item_iist_json(request):
    items = list(Item.objects.values("id", "item_name"))
    # return JsonResponse({"data":items})
    return JsonResponse(items, safe=False)



# -------------------------------- DRF code-----------------------------------------------

from .serializers import ItemSerializer
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView

# from rest_framework.generics import GenericAPIView
from rest_framework import generics

from rest_framework import viewsets


from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsOwnerOrReadOnly



# --------------------------get item list  and cretae item-------------------------

# # Function based--------
# @api_view(["GET","POST"])
# def item_iist_api(request):      # function based view 
#     if request.method == "GET":
#         items = Item.objects.all()
#         serializer =ItemSerializer(items, many= True) # many=True handling multiple objects (a queryset or list).
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = ItemSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)



# # class based ------------
# class ItemListApiView(APIView):   # class based views
#     def get(self,request):
#         items = Item.objects.all()
#         serializer =ItemSerializer(items, many= True) 
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = ItemSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


# generic class based-----------
class ItemListCreateAPI(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer



# --------------------------item get , update and delete  -------------------------
# # function based-----------
# @api_view(["GET", "PUT", "DELETE"])
# def item_detail_api(request, pk):            # function based view 
#     try:
#         item = Item.objects.get(pk=pk)
#     except Item.DoesNotExist:
#         return Response(
#             {"message": "Item not found"},
#             status=status.HTTP_404_NOT_FOUND
#         )

#     if request.method == "GET":
#         serializer =ItemSerializer(item)
#         return Response(serializer.data)
    
#     elif request.method == "PUT":
#         serializer = ItemSerializer(item, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#     elif request.method == "DELETE":
#         item.delete()
#         return Response({"messsage":"Item deleted Successfully"})



# # class based ----------
# class ItemDetailView(APIView):

#     def get_object(self,pk):
#         try:    
#             item = Item.objects.get(pk=pk)
#             return item
#         except Item.DoesNotExist:
#             return None
        
#     def get(self, request, pk):
#         item = self.get_object(pk)

#         if not item:
#             return Response(
#                 {"message": "Item not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = ItemSerializer(item)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def put(self, request, pk):
#         item = self.get_object(pk)

#         if not item:
#             return Response(
#                 {"message": "Item not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = ItemSerializer(item, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status= status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#     def delete(self,request, pk):
#         item = self.get_object(pk)
#         if not item:
#             return Response(
#                 {"message": "Item not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         item.delete()
#         return Response(
#             {"message": "Item deleted successfully"},
#             status=status.HTTP_204_NO_CONTENT
#         )



class ItemRetriveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset= Item.objects.all()
    serializer_class=ItemSerializer




# ---------------------- drf using one ViewSets for all type crud -----------
class ItemViewSet(viewsets.ModelViewSet):
        # authentication_classes = [TokenAuthentication]   # auth token
        # permission_classes = [IsAuthenticated]

        authentication_classes = [JWTAuthentication]  # JWT auth token
        permission_classes = [IsOwnerOrReadOnly]

        queryset = Item.objects.all()
        serializer_class = ItemSerializer
