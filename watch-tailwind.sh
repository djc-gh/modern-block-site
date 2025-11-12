#!/bin/bash
# Watch and rebuild Tailwind CSS on changes

cd "$(dirname "$0")/theme"
echo "Watching Tailwind CSS for changes..."
echo "Press Ctrl+C to stop"
./node_modules/.bin/tailwindcss -c ./tailwind.config.js -i ./static/src/styles.css -o ./static/css/dist/styles.css --watch
