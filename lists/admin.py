from django.contrib import admin
from . import models


@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):

    """List Admin Definition"""

    list_display = ("user", "count_products")

    filter_horizontal = ("products",)
