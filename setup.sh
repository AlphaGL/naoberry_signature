#!/bin/bash
# Vercel build script — installs deps, applies migrations, collects static files.
echo "BUILD START"

python3 -m pip install -r requirements.txt

# Apply database migrations (DATABASE_URL must be set in Vercel env vars)
python3 manage.py migrate --noinput

# Collect static files into staticfiles_build/static (served by the vercel.json route)
python3 manage.py collectstatic --noinput --clear

echo "BUILD END"
