from django.contrib import admin
from .models import Item, CartItem

# Register your models here.
admin.site.register(Item)
admin.site.register(CartItem)