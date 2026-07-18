"""
One-time import: loads every photo in ./images into the database with the
curated captions/categories, uploading through the configured storage
(Cloudinary when CLOUDINARY_URL is set, local ./media otherwise).

Usage:
    python manage.py seed            # skips anything already seeded
    python manage.py seed --reset    # wipes gallery/products/students/testimonials first
"""
from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from core.models import Product, SiteSettings, Student, Testimonial, Work

IMAGES = Path(__file__).resolve().parents[3] / "images"

# (filename, category, caption, aspect) — order here = display order.
WORKS = [
    ("work-01.jpg", "bridal", "Crowned for the aisle", "4/5"),
    ("work-24.jpg", "bridal", "The just-married glow", "3/4"),
    ("work-21.jpg", "bridal", "Trad day, main character", "3/4"),
    ("work-02.jpg", "bridal", "The white wedding glow", "4/5"),
    ("work-04.jpg", "owanbe", "Gele artistry in teal", "3/4"),
    ("work-05.jpg", "transform", "Before the magic", "4/5"),
    ("work-06.jpg", "transform", "…and after ✨", "4/5"),
    ("work-26.jpg", "glam", "Berry eyes, silk energy", "3/4"),
    ("work-18.jpg", "owanbe", "White gele, coral beads", "3/4"),
    ("work-20.jpg", "bridal", "Silver-beaded bride", "4/5"),
    ("work-08.jpg", "glam", "Soft glam, full attitude", "3/4"),
    ("work-22.jpg", "owanbe", "Mother of the day", "4/5"),
    ("work-03.jpg", "bridal", "Trad bride — coral & gold", "3/4"),
    ("work-09.jpg", "bridal", "The bride & her lilies", "3/4"),
    ("work-10.jpg", "glam", "Rosy soft glam", "4/5"),
    ("work-07.jpg", "bridal", "Coral crown, golden lids", "3/4"),
    ("work-13.jpg", "bridal", "Bouquet in hand, heart full", "3/4"),
    ("work-15.jpg", "glam", "Hot pink smoke", "4/5"),
    ("work-16.jpg", "owanbe", "Berry velvet & coral", "3/4"),
    ("work-17.jpg", "glam", "Soft waves, softer glam", "4/5"),
    ("work-11.jpg", "bridal", "Coral crown close-up", "1/1"),
    ("work-27.jpg", "glam", "Sculpted & soft", "4/5"),
    ("work-12.jpg", "bridal", "The morning of", "3/4"),
    ("work-28.jpg", "glam", "Amethyst shimmer", "3/4"),
    ("work-25.jpg", "bridal", "Glow behind the bouquet", "4/5"),
    ("work-19.jpg", "glam", "Mauve monochrome", "3/4"),
    ("work-29.jpg", "owanbe", "Lady in red", "4/5"),
    ("collection-01.jpg", "studio", "Inside the studio — the beauty wall", "3/4"),
    ("collection-02.jpg", "studio", "The full Naoberry kit", "3/4"),
]

TESTIMONIALS = [
    ("My makeup lasted from the church service till the after-party. People "
     "were still asking for her number at midnight.", "A Naoberry bride, Owerri"),
    ("She didn't change my face — she upgraded it. I looked like me, on my "
     "absolute best day.", "Birthday shoot client"),
    ("I joined the class as a complete novice. Two months later I charged my "
     "first paying client.", "Naoberry Academy student"),
]


class Command(BaseCommand):
    help = "Seed the database from the local ./images folder."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true",
                            help="Delete existing content before seeding.")

    def _attach(self, obj, field, filename):
        path = IMAGES / filename
        if not path.exists():
            self.stdout.write(self.style.WARNING(f"  missing: {filename} (skipped)"))
            return False
        with path.open("rb") as fh:
            getattr(obj, field).save(filename, File(fh), save=True)
        return True

    def handle(self, *args, **opts):
        if opts["reset"]:
            Work.objects.all().delete()
            Product.objects.all().delete()
            Student.objects.all().delete()
            Testimonial.objects.all().delete()
            self.stdout.write("Cleared existing content.")

        s = SiteSettings.load()
        for field, filename in [("hero_image", "hero.jpg"),
                                ("artist_image", "naomi.jpg"),
                                ("class_image", "class.jpg")]:
            if not getattr(s, field):
                self.stdout.write(f"Site image {field} <- {filename}")
                self._attach(s, field, filename)

        if not Work.objects.exists():
            for i, (filename, cat, cap, ar) in enumerate(WORKS):
                w = Work(caption=cap, category=cat, aspect=ar, order=(i + 1) * 10)
                self.stdout.write(f"Gallery {i + 1:02d} <- {filename}")
                if self._attach(w, "image", filename) is False:
                    continue
        else:
            self.stdout.write("Gallery already has content — skipped (use --reset to redo).")

        if not Product.objects.exists():
            for i in range(1, 11):
                filename = f"product-{i:02d}.jpg"
                p = Product(order=i * 10)
                self.stdout.write(f"Product {i:02d} <- {filename}")
                self._attach(p, "image", filename)
        else:
            self.stdout.write("Products already exist — skipped.")

        if not Student.objects.exists():
            for i in range(1, 5):
                filename = f"student-{i:02d}.jpg"
                st = Student(order=i * 10)
                self.stdout.write(f"Student {i:02d} <- {filename}")
                self._attach(st, "image", filename)
        else:
            self.stdout.write("Students already exist — skipped.")

        if not Testimonial.objects.exists():
            for i, (quote, author) in enumerate(TESTIMONIALS):
                Testimonial.objects.create(quote=quote, author=author, order=(i + 1) * 10)
            self.stdout.write("Seeded 3 sample testimonials — replace with real ones!")

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
