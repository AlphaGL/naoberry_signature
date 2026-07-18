from django import forms

from core.models import Product, SiteSettings, Student, Testimonial, Work


class BrandedFormMixin:
    """Adds the dashboard CSS classes to every widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "db-check")
            elif isinstance(widget, forms.ClearableFileInput):
                widget.attrs.setdefault("class", "db-file")
            elif isinstance(widget, (forms.Select,)):
                widget.attrs.setdefault("class", "db-input")
            elif isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("class", "db-input")
                widget.attrs.setdefault("rows", 4)
            else:
                widget.attrs.setdefault("class", "db-input")


class WorkForm(BrandedFormMixin, forms.ModelForm):
    class Meta:
        model = Work
        fields = ["image", "caption", "category", "aspect",
                  "instagram_link", "order", "is_published"]


class ProductForm(BrandedFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ["image", "name", "order", "is_published"]


class StudentForm(BrandedFormMixin, forms.ModelForm):
    class Meta:
        model = Student
        fields = ["image", "name", "order", "is_published"]


class TestimonialForm(BrandedFormMixin, forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["quote", "author", "order", "is_published"]


class SiteSettingsForm(BrandedFormMixin, forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            "phone_primary", "phone_secondary", "whatsapp_number", "whatsapp_link",
            "address_line1", "address_line2", "instagram_url", "facebook_url",
            "stat_looks", "stat_brides", "stat_students",
            "hero_image", "artist_image", "class_image",
        ]
