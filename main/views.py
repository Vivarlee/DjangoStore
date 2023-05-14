import datetime
import json
import numpy as np
from django.contrib.auth import login as logindj, authenticate, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from .models import Functions  # Item, Order
from .forms import FunctionsForm
from .NumMeth import *

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
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


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
        vertobussy = User.objects.create_user(username=request.POST['username'], password=request.POST['password'],
                                              email=request.POST['email'])
        vertobussy.save()
        logindj(request, vertobussy)
        return redirect('home')
    return render(request, 'main/register.html')


@require_POST
def checkusername(request):
    post = json.loads(request.body.decode("utf-8"))
    if User.objects.filter(username=post.get("username")).exists():
        return JsonResponse({"exists": True})
    return JsonResponse({"exists": False})


def sample_view(request):
    return render(request, 'main/base.html', {'current_user': request.user.username})


def calculator(request):
    return render(request, 'main/gauss.html')


def calc_gauss(request):
    rows, columns = map(int, request.GET['dim'].split(','))
    values=list(map(int,request.GET['values'].split(',')))
    matrix=[]
    for i in range(rows):
        matrix.append([])
        for j in range(columns + 1):
            matrix[-1].append(values[i*columns + j])

    error = ''
    try:
        result = gauss(rows,matrix)
        rounded_result = list(map(lambda x: round(x, 5), result))
        result = str(rounded_result)[1:-1]
    except ZeroDivisionError:
        error = "Division By Zero occured"
        result = ''
    return JsonResponse(data={'result': result, 'error': error})


def newton(request):
    return render(request, 'main/function_base.html', context={'name': "Newton's method"})


def calc_newton(request):
    try:
        result = newton_root(request.GET['expression'], float(request.GET['x0']), float(request.GET['atol']))
    except ValueError:
        result = 'Value Error'
    return JsonResponse(data={'result': str(result)})


def jacobi(request):
    return render(request, 'main/linear.html', context={'name': 'Jacobi method', 'calc_url': '/calc/jacobi'})


def calc_jacobi(request):
    A = np.array(list(map(float, request.GET['values'].split(','))), ndmin=2)
    rows, columns = map(int, request.GET['dim'].split(','))
    A.shape = (rows, columns)
    b = np.array(list(map(float, request.GET['b'].split(','))))

    error = ''
    if rows != columns:
        error = 'Jacobi method can be used with square matrices only'
        result = ''
    else:
        result = jacobi_roots(A, b)
        rounded_result = list(map(lambda x: round(x, 5), result))
        result = str(rounded_result)[1:-1]
        if 'nan' in result or 'inf' in result:
            error = 'This method is not applicable with these values'
            result = ''
    return JsonResponse({'result': result, 'error': error})

def seidel(request):
    return render(request, 'main/linear.html', context={'name': 'Gauss-Seidel method', 'calc_url': '/calc/seidel'})


def calc_seidel(request):
    A = np.array(list(map(float, request.GET['values'].split(','))), ndmin=2)
    rows, columns = map(int, request.GET['dim'].split(','))
    A.shape = (rows, columns)
    b = np.array(list(map(float, request.GET['b'].split(','))))

    error = ''
    if rows != columns:
        error = 'Gauss-Seidel method can be used with square matrices only'
        result = ''
    else:
        result = gauss_seidel_roots(A, b)
        rounded_result = list(map(lambda x: round(x, 5), result))
        result = str(rounded_result)[1:-1]
        if 'nan' in result or 'inf' in result:
            error = 'This method is not applicable with these values'
            result = ''
    return JsonResponse({'result': result, 'error': error})
