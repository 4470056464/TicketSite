from django.contrib import admin

from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display=['name','slug','price','capacity','available','created']
    list_filter=['available','created','updated']
    list_editable=['price','capacity','available']
    prepopulated_fields={'slug':('name',)}

admin.site.register(Product,ProductAdmin)
