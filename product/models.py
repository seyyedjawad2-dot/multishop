

from django.db import models


class Size(models.Model):
    title = models.CharField(max_length=20)
    def __str__(self):
        return self.title

class Color(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=20)
    price = models.IntegerField()
    description = models.TextField()
    discount = models.SmallIntegerField()
    image = models.ImageField(upload_to="products")
    size = models.ManyToManyField(Size,blank=True,null=True,related_name="products")
    color = models.ManyToManyField(Color,related_name="products")


    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"


    def __str__(self):
        return self.title


class Information(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="information",null=True)
    text = models.TextField()

    def __str__(self):
        return self.text[:30]