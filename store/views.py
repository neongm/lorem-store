from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse

# LOGIN STUFF
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# CART/ITEMS
from .models import CartItem, Item

# Create your views here.

def login(req):
    context = {}

    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(req, user)
            return redirect('cart')
        else:
            messages.info(req, 'user not found or password is incorrect')
            return redirect('login')
    else:
        return render(req, 'acc/login.html', context)


def register(req):
    context = {}

    if req.method == "POST":
        username = req.POST.get('username')
        password1 = req.POST.get('password1')
        password2 = req.POST.get('password2')
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(req, 'username already exists')
                print('user already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                print('registred '+ username)
                return redirect('login')
        else:
            messages.info(req, 'passwords are different')
            print('passwords are different')
            return redirect('register')
    else:
        return render(req, 'acc/register.html', context)


@login_required(login_url="login")
def logout(req):
    auth.logout(req)
    return redirect("store")

@login_required(login_url="login")
def cart(req):
    try:
        cart_items = CartItem.objects.filter(owner=req.user).order_by('-id')
        total_cost = sum([entry.item.price * entry.quantity for entry in cart_items])
    except CartItem.DoesNotExist:
        cart_items = []
        total_cost = 0

    context = {
        "cart_items": cart_items,
        "total_cost": total_cost
    }

    return render(req, 'store/cart.html', context)


def index(req):
    prods = Item.objects.order_by('id')

    context = {
        'products': prods
    }
    return render(req, 'store/index.html', context)

def delete_cart_item(req, item_id):
    cart_item_to_delete = CartItem.objects.filter(id=item_id).first()
    if req.user == cart_item_to_delete.owner:
        cart_item_to_delete.delete()
    return redirect('cart')

def add_cart_item(req):
    if req.method == "POST":
        item_id = req.POST.get('item_id')
        print(item_id)
        quantity = req.POST.get('quantity')
        print(quantity)
        item_to_add = Item.objects.get(id=item_id)
        print(item_to_add)
        try:
            existing_item = CartItem.objects.get(owner=req.user, item=item_to_add)
            existing_item.quantity = quantity
            existing_item.save()
        except CartItem.DoesNotExist:
            item = CartItem(
                owner = req.user,
                item = item_to_add,
                quantity=quantity,
            )
            item.save()

    return HttpResponseRedirect(reverse('item_detail', args=[req.POST.get('item_id')]))


def item_detail(req, item_id):
    context = {
        'item': Item.objects.get(id=item_id)
    }
    return render(req, "store/item_detail.html", context)