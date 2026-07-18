#!/bin/bash
# Vercel build script — installs deps, applies migrations, collects static files.
# Uses a throwaway venv in /tmp so install + run share one interpreter,
# sidestepping the externally-managed system Python on the build image.
set -e
echo "BUILD START"

if command -v uv >/dev/null 2>&1; then
  uv venv /tmp/buildenv
  . /tmp/buildenv/bin/activate
  uv pip install -r requirements.txt
else
  python3 -m venv /tmp/buildenv
  . /tmp/buildenv/bin/activate
  pip install -r requirements.txt
fi

# Apply database migrations (DATABASE_URL must be set in Vercel env vars)
python manage.py migrate --noinput

# Collect static files into staticfiles_build/static (served by the vercel.json route)
python manage.py collectstatic --noinput --clear

echo "BUILD END"
