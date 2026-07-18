from django.shortcuts import render

from .models import Product, SiteSettings, Student, Testimonial, Work


def home(request):
    settings_obj = SiteSettings.load()

    works = [
        {
            "src": w.image.url,
            "cat": w.category,
            "cap": w.caption,
            "ar": w.aspect,
            "link": w.instagram_link or settings_obj.instagram_url,
        }
        for w in Work.objects.filter(is_published=True)
    ]
    products = [p.image.url for p in Product.objects.filter(is_published=True)]
    students = [s.image.url for s in Student.objects.filter(is_published=True)]

    site_data = {
        "works": works,
        "products": products,
        "students": students,
        "whatsappNumber": settings_obj.whatsapp_number,
        "instagram": settings_obj.instagram_url,
    }

    context = {
        "s": settings_obj,
        "site_data": site_data,
        "testimonials": Testimonial.objects.filter(is_published=True),
        "works_count": len(works),
    }
    return render(request, "index.html", context)
