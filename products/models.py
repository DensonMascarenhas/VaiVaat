from django.db import models


class product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    discount = models.FloatField(default=1.0)
    gst = models.FloatField(default=1.0)
    purchase_price=models.FloatField()


class entry(models.Model):
     qty=models.IntegerField()
     price=models.FloatField()
     datie=models.CharField(max_length=100)
     name=models.CharField(max_length=100,default="null")


class stock_purchase(models.Model):
    item_id=models.IntegerField()
    item_name=models.CharField(max_length=100,default="null")
    qty=models.IntegerField()
    datie=models.CharField(max_length=50)
    price=models.FloatField()
    supplier=models.CharField(max_length=100,default="null")
    purchase_price=models.FloatField()

class credit(models.Model):
    name=models.CharField(max_length=50,default="null")
    phone=models.CharField(max_length=20)
    bill_amount=models.FloatField()
    paid_amount=models.FloatField()
    pending_amount=models.FloatField()
    datie=models.CharField(max_length=50)

class paytm(models.Model):
    phone=models.CharField(max_length=20)
    bill_amount = models.FloatField()
    already_amount=models.FloatField(default=0.0)
    balance=models.FloatField()
    datie=models.CharField(max_length=100,default="null")


class admin_credit(models.Model):
    supplier=models.CharField(max_length=100)
    total=models.FloatField()
    paid=models.FloatField()
    balance=models.FloatField()
    datie = models.CharField(max_length=100)


class paytm2(models.Model):
    supplier=models.CharField(max_length=100)
    bill_amount = models.FloatField()
    already_amount = models.FloatField(default=0.0)
    balance = models.FloatField()
    datie = models.CharField(max_length=100, default="null")


class shop_name(models.Model):
    name=models.CharField(max_length=100)
    info=models.CharField(max_length=200)