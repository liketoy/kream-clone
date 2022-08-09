from django.contrib import admin
from . import models


class PhotoInline(admin.StackedInline):

    model = models.Photo
    extra = 5


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ("__str__", "count_products")
    inlines = [
        PhotoInline,
    ]
    filter_horizontal = ("products",)
