import datetime

from django.contrib.auth import login as logindj, authenticate, logout
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from django.contrib.auth.models import User,Group
from .models import Functions  #Item, Order
from .forms import FunctionsForm
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
import json


# NOT A VIEW, TOO LAZY TO PUT THIS IN A PROPER PLACE
'''
def get_cart_items_amount(user):
    if user.is_anonymous:
        return 0

    filtered_orders = Order.objects.filter(user=user, ordered=False)
    if len(filtered_orders) == 0:
        return 0
    else:
        order: Order = filtered_orders[0]
        amount = 0
        for order_item in order.items.all():
            amount += order_item.quantity
        return amount
'''

def index(request):
    return render(request,'main/index.html')


def about(request):
    return render(request,'main/about.html')


# def shop(request):
#     context = {
#         'items': Item.objects.all(),
#         'cart_amount': get_cart_items_amount(request.user)
#     }
#
#     return render(request, 'main/home-page.html',context)





def login(request):
    if request.method == 'POST' and User.objects.filter(username=request.POST["username"]).exists():
        logout(request)
        usr = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if usr is not None:
            logindj(request, usr)
            return redirect('home')
    return render(request, 'main/login.html')


def register(request):
    if request.method == 'POST' and not User.objects.filter(username=request.POST["username"]).exists():
        vertobussy = User.objects.create_user(username=request.POST['username'],password=request.POST['password'],email=request.POST['email'])
        vertobussy.save()
        logindj(request,vertobussy)
        return redirect('home')
    return render(request, 'main/register.html')


@require_POST
def checkusername(request):
    post = json.loads(request.body.decode("utf-8"))
    if User.objects.filter(username=post.get("username")).exists():
        return JsonResponse({"exists": True})
    return JsonResponse({"exists": False})


def sample_view(request):
    return render(request,'main/base.html',{'current_user': request.user.username})
