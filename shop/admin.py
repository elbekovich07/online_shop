from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Product, Category, Comment

admin.site.unregister(Group)


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'price', 'updated_at', 'image_tag')
    list_filter = ('updated_at', 'price')
    search_fields = ('name', 'description')
    ordering = ('-updated_at',)

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:50px; max-height:50px"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'


class ProductResource(resources.ModelResource):
    class Meta:
        model = Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)
    ordering = ('-created_at',)
    list_filter = ('created_at',)


admin.site.register(Comment)
