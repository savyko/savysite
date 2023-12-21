from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    products = Product.objects.all()
    context= {'products': products}
    return render(request, 'app/home.html', context)
def base(request):
    return render(request, 'app/base.html')
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        order = {'get_cart_items': 0, 'get_cart_total':0}
        items = []

    context = {'items': items, 'order': order}
    return render(request, 'app/cart.html', context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        order = {'get_cart_items': 0, 'get_cart_total':0}
        items = []

    context = {'items': items, 'order': order}
    return render(request, 'app/checkout.html', context)
def brse(request):
    return render(request, 'app/course/brse.html')
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer =  request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action =='add':
        print("item is added..........", orderItem.quantity)
        orderItem.quantity +=1
    elif action =='remove':
        print("item is removed..........")
        orderItem.quantity -=1
    else:
        print("item unknown..........")
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse('added', safe=False)


@csrf_exempt  # Bỏ qua kiểm tra CSRF để đơn giản hóa ví dụ. Không nên sử dụng trong môi trường thực tế mà không có CSRF bảo vệ.
def update_cart(request):
    data = {'message': 'Error'}
    if request.method == 'POST':
        product_id = request.POST.get('productId')
        action = request.POST.get('action')

        try:
            product = Product.objects.get(id=product_id)
            user = request.user
            order, created = Order.objects.get_or_create(user=user, complete=False)
            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

            if action == 'add':
                order_item.quantity += 1
            elif action == 'remove':
                order_item.quantity -= 1

            if order_item.quantity <= 0:
                order_item.delete()
            else:
                order_item.save()

            data = {'message': 'Success'}
        except Exception as e:
            data = {'message': str(e)}

    return JsonResponse(data)
