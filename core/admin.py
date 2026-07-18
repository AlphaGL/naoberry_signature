"""Django's built-in admin — kept as a technical backup at /django-admin/.
The everyday admin experience is the custom dashboard at /dashboard/."""
from django.contrib import admin

from .models import Product, SiteSettings, Student, Testimonial, Work


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ("caption", "category", "order", "is_published")
    list_editable = ("order", "is_published")
    list_filter = ("category", "is_published")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("__str__", "order", "is_published")
    list_editable = ("order", "is_published")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "order", "is_published")
    list_editable = ("order", "is_published")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("__str__", "order", "is_published")
    list_editable = ("order", "is_published")


admin.site.register(SiteSettings)
