from django.contrib import admin,messages
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from . import models
# Register your models here.

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','price','collection_title']
    list_editable = ['price']
    list_per_page = 10
    list_filter = ['collection','last_update']
    search_fields =['title']

    def collection_title(self, product):
        return product.collection.title

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{} Products</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'quantity','status']
    
    