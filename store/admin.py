from django import forms
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import *

admin.site.register(Category, MPTTModelAdmin)

"many part of the relationship"
class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline,
    ]

"many part of the relationship"
class ProductImageInline(admin.TabularInline):
    model = ProductImage

"many part of the relationship"
class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline,
    ]
