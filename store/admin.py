from django.contrib import admin
from .models import *


class PictureInline(admin.StackedInline):
    model = Image

class ProductAdmin(admin.ModelAdmin):
    inlines = [PictureInline]

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'active']
    list_filter = ['active']
    search_fields = ['code']

admin.site.register(Coupon, CouponAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Rating)
