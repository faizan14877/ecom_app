from django.db import models

# Create your models here.


class Product(models.Model):
    product_id = models.AutoField
    desc = models.CharField(max_length=1000)
    name = models.CharField(max_length=100)
    pub_date = models.DateField()
    price = models.IntegerField(default=0)
    category = models.CharField(max_length=50, default='')
    subcategory = models.CharField(max_length=50, default='')
    image = models.ImageField(upload_to='shop/images', default='')

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.IntegerField(max_length=100)
    desc = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000, default="", blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)

    
class OrderUpdate(models.Model):
    order_id = models.IntegerField(max_length=100)
    update_id = models.AutoField(primary_key=True)
    update_desc = models.CharField(max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
