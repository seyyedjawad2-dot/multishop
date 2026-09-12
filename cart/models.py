from django.db import models

from account.models import User
from product.models import Product


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='orders',verbose_name= 'کاربر')
    total_price=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False,verbose_name= 'پرداخت شده')


    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name='سفارش'
        verbose_name_plural = 'سفارشات'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='items',verbose_name= 'محصول')
    size=models.CharField(max_length=5,verbose_name='سایز',blank=True,default='',null=True)
    color = models.CharField(max_length=5,verbose_name= 'رنگ',blank=True,default='',null=True)
    quantity = models.SmallIntegerField(verbose_name= 'تعداد')
    price=models.PositiveIntegerField(verbose_name= 'قیمت')


    class Meta:
        verbose_name = 'ایتم'
        verbose_name_plural = 'آیتم ها'


class DiscountCode(models.Model):
    name= models.CharField(max_length=10,unique=True)
    discount = models.SmallIntegerField(default=0)
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.name


