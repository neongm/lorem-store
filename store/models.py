from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Item(models.Model):
    # id = models.AutoField(primary_key=True) - here by default
    name = models.CharField('Item Name', max_length=60, default="Placeholder")
    sentence = models.CharField('Item Sentence', max_length=60)
    img_url = models.URLField('Item Image Url')
    descripotion = models.TextField('Item Description')
    price = models.IntegerField()

    def __str__(self):
        return f"({self.price}) {self.name} - {self.sentence}"


class CartItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

