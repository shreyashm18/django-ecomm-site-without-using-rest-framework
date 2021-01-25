from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Category(models.Model):
    category_name=models.CharField(null=False,blank=False,max_length=200)

    def __str__(self):
        return self.category_name

    @property
    def product(self):
        return self.products_set.all()



class Products(models.Model):
    product_name=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return self.product_name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=datetime.now)
    total = models.FloatField(blank=True, null= True, default=0)
    discounted_price = models.FloatField(blank=True, null= True, default=0)

    def __str__(self):
        return self.cart_name

    @property
    def cartitem(self):
        return self.cartitems_set.all()

class Cartitems(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    cart_name = models.CharField(max_length=200)
    item_name = models.CharField(max_length=200)
    item_price = models.FloatField()
    final_price = models.FloatField(default = 100)
    qnty = models.IntegerField(default=1)
    prod_id = models.IntegerField()

    def __str__(self):
        return self.item_name + "-" + self.cart_name


@receiver(post_save, sender = User)
def user_is_created(sender, instance, created, **kwargs):
    print(instance)
    if created:
        cart = Cart.objects.create(user = instance,cart_name = str(instance))