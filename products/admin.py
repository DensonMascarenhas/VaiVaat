from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import product

class productadmin(admin.ModelAdmin):
    list_display = ('name','purchase_price','price','stock','discount')




admin.site.register(product,productadmin)