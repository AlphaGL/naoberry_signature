# Naoberry Signature — Django site

Portfolio + booking site for Naoberry Signature (Owerri makeup studio), with a
custom admin dashboard at `/dashboard/`, Cloudinary image hosting, Postgres,
deployed on Vercel.

## Project layout

| Path | What it is |
| --- | --- |
| `core/` | Models (gallery, products, students, testimonials, site settings) + public view |
| `dashboard/` | The custom admin (login, CRUD, show/hide, site settings) |
| `templates/index.html` | The public website |
| `templates/dashboard/` | Admin screens |
| `static/` | CSS / JS / favicon |
| `images/` | Original photos — used once by `python manage.py seed` |
| `vercel.json`, `setup.sh` | Vercel deployment config |

## Run locally

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env          # then edit .env
python manage.py migrate
python manage.py seed           # imports every photo in ./images with captions
python manage.py createsuperuser
python manage.py runserver
```

- Website: http://127.0.0.1:8000/
- Admin dashboard: http://127.0.0.1:8000/dashboard/
- (Backup Django admin: /django-admin/)

Without `DATABASE_URL`/`CLOUDINARY_URL` in `.env`, it uses sqlite + local
`./media` uploads — perfect for development.

## Deploy to Vercel

### 1. Create the external services (both free tiers are fine)

- **Postgres** — create a database on Neon (what Vercel Postgres uses) or
  Supabase, copy the connection string (`postgres://...`).
- **Cloudinary** — create an account, copy the `CLOUDINARY_URL`
  (`cloudinary://API_KEY:API_SECRET@CLOUD_NAME`) from the dashboard.

### 2. Set environment variables in Vercel

Project → Settings → Environment Variables:

| Name | Value |
| --- | --- |
| `SECRET_KEY` | a long random string (`python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`) |
| `DEBUG` | `False` |
| `DATABASE_URL` | the Postgres connection string |
| `CLOUDINARY_URL` | the Cloudinary URL |
| `SITE_DOMAIN` | *(optional)* your custom domain, e.g. `naoberrysignature.com` |

### 3. Push and deploy

```bash
git add -A && git commit -m "Django backend"
git push
```

Import the repo in Vercel (or `npx vercel`). The build runs `setup.sh`:
installs requirements → `migrate` → `collectstatic`. `vercel.json` routes
`/static/*` to the collected files and everything else to Django.

### 4. First-time production setup (run once, from your PC)

Point your local shell at the production database, then create the admin
user and import all the photos to Cloudinary:

```bash
# in .env, temporarily set the production DATABASE_URL and CLOUDINARY_URL
python manage.py migrate
python manage.py createsuperuser     # Naomi's login
python manage.py seed                # uploads all ./images photos to Cloudinary
# then restore your local .env
```

After that, everything is managed from `https://your-site.vercel.app/dashboard/`.

## The dashboard

- **Overview** — one card per content type with live counts.
- **Gallery Looks / Products / Students / Testimonials** — add, edit, delete,
  and one-click **Hide/Show** (hide keeps the photo saved but removes it from
  the site). `order` controls position; the first 12 published gallery looks
  are the homepage storefront.
- **Site Settings** — phone numbers, WhatsApp number/link, address, social
  links, the three homepage stats, and the hero/artist/class photos.

## Notes

- Product cards are numbered; the WhatsApp enquiry message quotes the number
  **and** links the product's Cloudinary photo, so Naomi sees exactly which
  product the customer means.
- Testimonials currently contain 3 sample quotes from `seed` — replace them
  with real client words in the dashboard before launch.
