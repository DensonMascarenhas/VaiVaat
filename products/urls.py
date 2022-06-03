from django.urls import path
from . import views
urlpatterns=[
    path('', views.index),
    path('news/', views.news),
    path('main/',views.main),
    path('sub/', views.sub),
    path('passing/',views.passing),
    path('less/',views.less),
    path('daily/',views.daily),
    path('add_stock/',views.add_stock),
    path('add_db/',views.add_db),
    path('purchase_bill',views.purchase_bill),
    path("sales",views.sales),
    path("report", views.report),
    path("show_rep", views.show_rep),
    path("find_sale", views.find_sale),
    path("credit", views.credit),
    path("pay_credit", views.pay_credit),
    path("paytm", views.paytm),
    path("admin_credit", views.admin_credit),
    path("view-credit", views.view_credit),
    path("paytm2", views.paytm2),
    path("end", views.end),
    path("stop", views.stop),
    path("setting", views.setting),




]