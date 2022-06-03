"""shop_assist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from products.views import index,talk,news,main,sub,passing,setting,less,daily,add_stock,add_db,purchase_bill,sales,report,show_rep,find_sale,credit,pay_credit,paytm,admin_credit,view_credit,paytm2,end,stop

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('', index,name="index"),
    path('talk',talk),
    path('news',news,name='news'),
    path('main',main,name='main'),
    path('sub', sub),
    path('passing',passing),
    path('less',less,name='less'),
    path('daily',daily,name='daily'),
    path('add_stock',add_stock,name='add_stock'),
    path('add_db',add_db,name="add_db"),
    path('purchase_bill',purchase_bill,name="purchase_bill"),
    path('sales',sales,name="sales"),
    path('report',report,name="report"),
    path('show_rep',show_rep,name="show_rep"),
    path('find_sale',find_sale,name="find_sale"),
    path('credit',credit,name="credit"),
    path('pay_credit',pay_credit,name="pay_credit"),
    path('paytm',paytm,name="paytm"),
    path('admin_credit', admin_credit, name="admin_credit"),
    path('view-credit', view_credit, name="view-credit"),
    path('paytm2',paytm2,name="paytm2"),
    path('end',end,name="end"),
    path('stop',stop,name="stop"),
    path('setting', setting, name="setting"),
]
