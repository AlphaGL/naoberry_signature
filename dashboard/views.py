"""
The custom admin dashboard.

One SECTIONS registry drives every content type, so the list/add/edit/delete
screens look and behave identically — the admin learns it once and can manage
everything.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from core.models import Product, SiteSettings, Student, Testimonial, Work

from .forms import (ProductForm, SiteSettingsForm, StudentForm,
                    TestimonialForm, WorkForm)

SECTIONS = {
    "gallery": {
        "model": Work,
        "form": WorkForm,
        "title": "Gallery Looks",
        "singular": "look",
        "icon": "🖼",
        "help": ("Photos in the portfolio. Lower order numbers show first — "
                 "the first 12 published looks appear before the “Show more” button."),
        "has_image": True,
    },
    "products": {
        "model": Product,
        "form": ProductForm,
        "title": "Beauty Bar Products",
        "singular": "product",
        "icon": "🛍",
        "help": ("Product photos for the shop section. Cards are numbered by "
                 "order — customers tap one to ask the price on WhatsApp."),
        "has_image": True,
    },
    "students": {
        "model": Student,
        "form": StudentForm,
        "title": "Certified Students",
        "singular": "student",
        "icon": "🎓",
        "help": "Graduate photos (holding their certificates) shown in the students section.",
        "has_image": True,
    },
    "testimonials": {
        "model": Testimonial,
        "form": TestimonialForm,
        "title": "Testimonials",
        "singular": "testimonial",
        "icon": "💬",
        "help": "Short client quotes that rotate on the homepage.",
        "has_image": False,
    },
}


def _section_or_404(key):
    if key not in SECTIONS:
        raise Http404
    return SECTIONS[key]


@login_required
def home(request):
    cards = []
    for key, cfg in SECTIONS.items():
        cards.append({
            "key": key,
            "title": cfg["title"],
            "icon": cfg["icon"],
            "help": cfg["help"],
            "count": cfg["model"].objects.count(),
            "published": cfg["model"].objects.filter(is_published=True).count(),
        })
    return render(request, "dashboard/home.html", {"cards": cards})


@login_required
def section_list(request, section):
    cfg = _section_or_404(section)
    items = cfg["model"].objects.all()
    return render(request, "dashboard/list.html", {
        "cfg": cfg, "section": section, "items": items,
    })


@login_required
def section_add(request, section):
    cfg = _section_or_404(section)
    form = cfg["form"](request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"New {cfg['singular']} added ✔")
        return redirect("dashboard:list", section=section)
    return render(request, "dashboard/form.html", {
        "cfg": cfg, "section": section, "form": form, "obj": None,
    })


@login_required
def section_edit(request, section, pk):
    cfg = _section_or_404(section)
    obj = get_object_or_404(cfg["model"], pk=pk)
    form = cfg["form"](request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{cfg['singular'].capitalize()} updated ✔")
        return redirect("dashboard:list", section=section)
    return render(request, "dashboard/form.html", {
        "cfg": cfg, "section": section, "form": form, "obj": obj,
    })


@login_required
def section_delete(request, section, pk):
    cfg = _section_or_404(section)
    obj = get_object_or_404(cfg["model"], pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, f"{cfg['singular'].capitalize()} deleted.")
        return redirect("dashboard:list", section=section)
    return render(request, "dashboard/confirm_delete.html", {
        "cfg": cfg, "section": section, "obj": obj,
    })


@login_required
def section_toggle(request, section, pk):
    """One-click show/hide on the website."""
    cfg = _section_or_404(section)
    obj = get_object_or_404(cfg["model"], pk=pk)
    if request.method == "POST":
        obj.is_published = not obj.is_published
        obj.save()
        state = "visible on the site" if obj.is_published else "hidden from the site"
        messages.success(request, f"{cfg['singular'].capitalize()} is now {state}.")
    return redirect("dashboard:list", section=section)


@login_required
def site_settings(request):
    obj = SiteSettings.load()
    form = SiteSettingsForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Site settings saved ✔")
        return redirect("dashboard:settings")
    return render(request, "dashboard/settings.html", {"form": form, "obj": obj})
