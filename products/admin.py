from django.contrib import admin
from products.models import Brand, Category, Photo, Product


class PhotoInline(admin.TabularInline):

    model = Photo
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    inlines = [
        PhotoInline,
    ]
    list_display = ("name_en", "name_kr", "brand")
    search_fields = ("brand__name", "name_en", "name_kr")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "count_products")
