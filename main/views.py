import datetime

from django.contrib.auth import login as logindj, authenticate, logout
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from django.contrib.auth.models import User,Group
from .models import Item, Order
from .forms import ItemsForm
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
import json


# NOT A VIEW, TOO LAZY TO PUT THIS IN A PROPER PLACE
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


def index(request):
    return render(request,'main/index.html')


def about(request):
    return render(request,'main/about.html')


def shop(request):
    context = {
        'items': Item.objects.all(),
        'cart_amount': get_cart_items_amount(request.user)
    }

    return render(request, 'main/home-page.html',context)


def editor(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    error = ''
    if request.method == 'POST':
        form = ItemsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form.fields)
        else:
            error = 'Not a valid form'

    form = ItemsForm()
    context={
        'form': form,
        'error': error

    }
    return render(request, 'main/editing.html',context)


@require_POST
def delete_item(request):
    Item.objects.get(pk=request.POST["item"]).delete()
    return redirect("shop")


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


def cart(request):
    if request.user.is_anonymous:
        return redirect('login')

    filtered_orders = Order.objects.filter(user=request.user, ordered=False)
    total_cost = 0
    if len(filtered_orders) == 0:
        order = None
    else:
        order = filtered_orders[0].items.all().order_by("added")
        for orderitem in order:
            total_cost += orderitem.total_cost

    return render(request,'main/cart.html', {'order': order,
                                             'cart_amount': get_cart_items_amount(request.user),
                                             'total_cost': total_cost})


@require_POST
def add_to_cart(request):
    if request.user.is_anonymous:
        return redirect("login")

    if request.headers.get('X-CSRFtoken') is not None:
        post = json.loads(request.body.decode("utf-8"))
    else:
        post = request.POST

    filtered_orders = Order.objects.filter(user=request.user, ordered=False)
    if len(filtered_orders) == 0:
        order: Order = Order.objects.create(user=request.user)
        order.save()
    else:
        order: Order = filtered_orders[0]

    item_to_add = Item.objects.get(pk=post["item_id"])
    order_items = order.items.filter(item=item_to_add)
    if len(order_items) == 0:
        item = order.items.create(item=item_to_add)
        item.save()
    else:
        order_items[0].quantity += 1
        order_items[0].save()

    if request.headers.get('X-CSRFtoken') is not None:
        return JsonResponse({})

    return redirect(request.META['HTTP_REFERER'])


@require_POST
def remove_from_cart(request):
    if request.user.is_anonymous:
        return redirect("login")

    if request.headers.get('X-CSRFtoken') is not None:
        post = json.loads(request.body.decode("utf-8"))
    else:
        post = request.POST

    filtered_orders = Order.objects.filter(user=request.user, ordered=False)
    if len(filtered_orders) == 0:
        return HttpResponse(500)

    order: Order = filtered_orders[0]

    item_to_remove = Item.objects.get(pk=post["item_id"])
    order_item = order.items.get(item=item_to_remove)
    order_item.quantity -= 1

    if order_item.quantity < 1:
        order_item.delete()

        if len(order.items.all()) == 0:
            order.delete()
    else:
        order_item.save()

    if request.headers.get('X-CSRFtoken') is not None:
        return JsonResponse({})

    return redirect(request.META['HTTP_REFERER'])


@require_POST
def delete_from_cart(request):
    if request.user.is_anonymous:
        return HttpResponseForbidden()

    filtered_orders = Order.objects.filter(user=request.user, ordered=False)
    if len(filtered_orders) == 0:
        return HttpResponse(status=400)

    order: Order = filtered_orders[0]
    print(request.POST['item'])
    try:
        order_item = order.items.get(pk=request.POST['item'])
        order_item.delete()

        if len(order.items.all()) == 0:
            order.delete()

        return redirect(request.META['HTTP_REFERER'])
    except:  # don't know what error get() can return, so i'll leave it like this for now
        return HttpResponse(status=400)


@require_POST
def place_order(request):
    if request.user.is_anonymous:
        return HttpResponseForbidden()

    filtered_orders = Order.objects.filter(user=request.user, ordered=False)
    if len(filtered_orders) == 0:
        return HttpResponse(status=400)

    order: Order = filtered_orders[0]
    order.ordered = True
    order.ordered_date = datetime.datetime.now()
    order.save()

    return redirect("shop")
