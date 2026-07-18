#!/bin/bash
# Vercel build script — installs deps, applies migrations, collects static files.
set -e
echo "BUILD START"

# Vercel's build image ships a uv-managed Python that blocks plain `pip install`.
# Prefer uv; fall back to pip with the documented override flag.
if command -v uv >/dev/null 2>&1; then
  uv pip install --system -r requirements.txt
else
  python3 -m pip install --break-system-packages -r requirements.txt
fi

# Apply database migrations (DATABASE_URL must be set in Vercel env vars)
python3 manage.py migrate --noinput

# Collect static files into staticfiles_build/static (served by the vercel.json route)
python3 manage.py collectstatic --noinput --clear

echo "BUILD END"
