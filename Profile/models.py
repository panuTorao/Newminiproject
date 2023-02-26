from django.db import models

# Create your models here.
import datetime
from django.db import models
from django.utils import timezone
from django.db.models import F, Sum, Count

class Categories(models.Model):
    name = models.CharField(max_length=50, default="")
    desc = models.TextField(max_length=400, default="")
    def __str__(self):
        return str(self.id) + ":" + self.name
    def getCountProduct(self):
        count = Products.objects.filter(category=self).aggregate(count=Count('pid'))
        return count['count']
    def getCountProducts(self):
        categories = Categories.objects.annotate(number_of_product=Count('product'))

class Products(models.Model):
    pid = models.CharField(max_length=13, primary_key=True, default="")
    name = models.CharField(max_length=50, default="")
    detail = models.CharField(max_length=200, default="")
    price=models.FloatField(default=0.00)
    net = models.IntegerField(default=0)
    picture = models.ImageField(upload_to ='static/products/', default="")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.pid + ":" + self.name + ", " + str(self.price)

















