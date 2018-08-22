from django.contrib import admin
from .models import User, Category, Goods

admin.site.register([User, Category, Goods])
#
#
# @admin.register(Goods)
# class GoodsAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'thumb')
