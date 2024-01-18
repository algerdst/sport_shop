from django.contrib import admin

from .models import (Brand, Category, Gallery, ItemType, PopularCategory,
                     Product)

admin.site.register(PopularCategory)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'slug']
    prepopulated_fields = {"slug": ("brand_name",)}


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'slug']
    filter_horizontal = ['categories']
    prepopulated_fields = {"slug": ("type_name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']
    prepopulated_fields = {"slug": ("category_name",)}


class GalleryInline(admin.TabularInline):
    model = Gallery


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'type_product', 'category', 'price', 'quantity_in_stock']
    prepopulated_fields = {"slug": ("name",)}
    inlines = [GalleryInline]
