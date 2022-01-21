from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Avg
import json
import datetime
from .models import *
from .forms import RatingForm, CouponForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def store(request):
    products = Product.objects.all()
    images = Image.objects.filter(default=True)
    context = {'products': products, 'images': images}
    return render(request, 'store/store.html', context)

def cart(request):
    products = Product.objects.all()
    images = Image.objects.filter(default=True)
    coupon = ''
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code=code, active=True)
            except Coupon.DoesNotExist:
                messages.info(request, 'Please enter valid coupon!')
                print('no coupon')
        else:
            messages.info(request, 'No coupon')
            print(form.errors.as_data())
        try:
            orderitems = OrderItem.objects.filter(order_id=order)
            for item in orderitems:
                item.coupon_id = coupon
                item.save()
            messages.success(request, "Coupon applied")
        except OrderItem.DoesNotExist:
            print('order item does not exist')

    context = {'items': items, 'order': order, 'images': images, 'products': products}
    return render(request, 'store/cart.html', context)

def add_variable_to_context(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'order': order}
    return context

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        images = Image.objects.filter(default=True)
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'items': items, 'order': order, 'images': images}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == order.get_cart_total_discounted:
            order.complete = True
        order.save()
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in')
    return JsonResponse('Payment complete!', safe=False)

def detail(request, pk):
    product = Product.objects.get(id=pk)
    images = Image.objects.filter(product_id=product)
    ratings = Rating.objects.filter(product_id=pk)
    try:
        average = ratings.aggregate(avg=Avg("rating"))
        average = round(average['avg'], 2)
    except Exception:
        average = 0
    context = {'products': product, 'images': images, 'rating': ratings, 'avg': average}
    return render(request, 'store/detail.html', context)

@login_required
def review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.customer_id = request.user.customer.id
            new_review.product_id = pk
            new_review.save()
            return redirect(product)
    else:
        form = RatingForm()
    context = {'review_form': form}
    return render(request, 'store/review.html', context)


