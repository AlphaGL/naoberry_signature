"""
Everything the admin can edit from the dashboard lives here.

Ordering convention: every list model has an `order` field — lower numbers
appear first on the website. The dashboard explains this to the admin.
"""
from django.db import models

INSTAGRAM_DEFAULT = "https://www.instagram.com/naoberry_signature"


class SiteSettings(models.Model):
    """Singleton: contact details, socials, stats and the fixed site photos."""

    phone_primary = models.CharField(
        max_length=20, default="08149946164",
        help_text="Main phone number shown on the site.")
    phone_secondary = models.CharField(
        max_length=20, blank=True, default="09150512286",
        help_text="Second phone number (optional).")
    whatsapp_number = models.CharField(
        max_length=20, default="2348149946164",
        help_text="WhatsApp number in international format, digits only "
                  "(e.g. 2348149946164). Used for all booking buttons.")
    whatsapp_link = models.URLField(
        blank=True, default="https://wa.me/message/IJYB6PG5A4FGM1",
        help_text="Official WhatsApp business short link (wa.me/message/...). "
                  "Leave empty to use the WhatsApp number instead.")
    address_line1 = models.CharField(
        max_length=120, default="No. 38 Okigwe Road, beside DSTV Office")
    address_line2 = models.CharField(
        max_length=120, default="by IMSU Junction, Orji — Owerri, Imo State")
    instagram_url = models.URLField(default=INSTAGRAM_DEFAULT)
    facebook_url = models.URLField(
        default="https://web.facebook.com/profile.php?id=61557655057446")

    stat_looks = models.PositiveIntegerField(
        default=200, help_text='"Signature looks" number shown on the homepage.')
    stat_brides = models.PositiveIntegerField(
        default=100, help_text='"Brides & celebrants" number.')
    stat_students = models.PositiveIntegerField(
        default=50, help_text='"Students trained" number.')

    hero_image = models.ImageField(
        upload_to="site/", blank=True, null=True,
        help_text="The big photo at the top of the site (portrait works best).")
    artist_image = models.ImageField(
        upload_to="site/", blank=True, null=True,
        help_text='Photo of Naomi in "The Artist" section.')
    class_image = models.ImageField(
        upload_to="site/", blank=True, null=True,
        help_text="Photo in the makeup classes section.")

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1  # enforce a single row
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def booking_link(self):
        return self.whatsapp_link or f"https://wa.me/{self.whatsapp_number}"


class Work(models.Model):
    """A look in the portfolio gallery."""

    CATEGORIES = [
        ("bridal", "Bridal"),
        ("owanbe", "Owanbe"),
        ("glam", "Glam"),
        ("transform", "Before / After"),
        ("studio", "Studio"),
    ]
    SHAPES = [
        ("4/5", "Tall (4:5)"),
        ("3/4", "Taller (3:4)"),
        ("1/1", "Square (1:1)"),
    ]

    image = models.ImageField(upload_to="works/")
    caption = models.CharField(
        max_length=80, help_text='Short caption shown on the photo, e.g. "Crowned for the aisle".')
    category = models.CharField(max_length=12, choices=CATEGORIES, default="glam")
    aspect = models.CharField(
        max_length=4, choices=SHAPES, default="4/5",
        help_text="Tile shape in the gallery grid — mixing shapes looks best.")
    instagram_link = models.URLField(
        default=INSTAGRAM_DEFAULT,
        help_text="Link to this exact Instagram post (or leave the profile link).")
    order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers show first. The first 12 are on the front page.")
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Gallery look"
        verbose_name_plural = "Gallery looks"

    def __str__(self):
        return f"{self.caption} ({self.get_category_display()})"


class Product(models.Model):
    """A Beauty Bar product — image only; enquiries go to WhatsApp."""

    image = models.ImageField(upload_to="products/")
    name = models.CharField(
        max_length=80, blank=True,
        help_text="Optional — shown to you in the dashboard only; the site shows numbered cards.")
    order = models.PositiveIntegerField(
        default=0, help_text="Lower numbers show first (this sets the № on the card).")
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name or f"Product #{self.pk}"


class Student(models.Model):
    """A certified graduate photo (usually holding their certificate)."""

    image = models.ImageField(upload_to="students/")
    name = models.CharField(
        max_length=80, blank=True,
        help_text="Optional — for your own reference in the dashboard.")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Certified student"

    def __str__(self):
        return self.name or f"Student #{self.pk}"


class Testimonial(models.Model):
    quote = models.TextField(help_text="What the client said — keep it short and real.")
    author = models.CharField(
        max_length=80, help_text='Who said it, e.g. "A Naoberry bride, Owerri".')
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first.")
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"“{self.quote[:40]}…” — {self.author}"
