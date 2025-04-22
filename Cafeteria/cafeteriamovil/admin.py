from django.contrib import admin
from .models import Account_Detail, User, Promotions, Product_Detail, Product, Order, OrderDetail, Reviews
# Register your models here.

admin.site.register(Account_Detail)
admin.site.register(User)
admin.site.register(Promotions)
admin.site.register(Product_Detail)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Reviews)

