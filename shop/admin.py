from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from import_export import resources
from import_export.admin import  ImportExportMixin

from .models import Product, Category, Comment

admin.site.unregister(Group)

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


@admin.register(Product)
class ProductAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = ProductResource
    list_display = ('name', 'price', 'updated_at', 'image_tag')
    list_filter = ('updated_at', 'price')
    search_fields = ('name', 'description')
    ordering = ('-updated_at',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:50px; max-height:50px"/>'.format(obj.image.url))
        return '-'

    image_tag.short_description = 'Image'



@admin.register(Category)
class CategoryAdmin(ImportExportMixin,SortableAdminMixin, admin.ModelAdmin):
    resource_class = CategoryResource
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)
    ordering = ('-created_at',)
    list_filter = ('created_at',)



@admin.register(Comment)
class CommentAdmin(SortableAdminMixin,ImportExportMixin,admin.ModelAdmin):
    list_display = ('full_name', 'content', 'created_at')
    search_fields = ('text',)
    ordering = ('-created_at',)
    list_filter = ('created_at',)



