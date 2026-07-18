"""WSGI entry point. Vercel's @vercel/python builder looks for `app`."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "naoberry.settings")

application = get_wsgi_application()
app = application
