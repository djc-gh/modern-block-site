#!/bin/bash
# Build Tailwind CSS for production

PROJECT_DIR="$(dirname "$0")"
cd "$PROJECT_DIR"

echo "Building Tailwind CSS..."
cd theme
./node_modules/.bin/tailwindcss -c ./tailwind.config.js -i ./static/src/styles.css -o ./static/css/dist/styles.css --minify
echo "Tailwind CSS built successfully!"

# Collect static files
cd ..
echo "Collecting static files..."
source .venv/bin/activate
python manage.py collectstatic --noinput
echo "Done!"
