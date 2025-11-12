# Tailwind CSS Setup

## Overview
This project uses Tailwind CSS v3 for styling. The Tailwind CSS is compiled from source files in the `theme/static/src/` directory.

## Files Structure
```
theme/
├── static/
│   ├── src/
│   │   └── styles.css          # Source Tailwind CSS file
│   └── css/
│       └── dist/
│           └── styles.css      # Compiled/built CSS file
└── package.json                # Node.js dependencies

tailwind.config.js              # Tailwind configuration
```

## Building Tailwind CSS

### Production Build
To build Tailwind CSS for production (minified):
```bash
./build-tailwind.sh
```

Or manually:
```bash
cd theme
npx tailwindcss -c ../tailwind.config.js -i ./static/src/styles.css -o ./static/css/dist/styles.css --minify
cd ..
python manage.py collectstatic --noinput
```

### Development Watch Mode
To watch for changes and automatically rebuild:
```bash
./watch-tailwind.sh
```

Or manually:
```bash
cd theme
npx tailwindcss -c ../tailwind.config.js -i ./static/src/styles.css -o ./static/css/dist/styles.css --watch
```

## Making Changes

1. **Edit styles**: Modify `theme/static/src/styles.css` or your HTML templates
2. **Rebuild**: Run `./build-tailwind.sh` or use watch mode
3. **Collect static**: If in production, run `python manage.py collectstatic`

## Custom Configuration

The Tailwind configuration in `tailwind.config.js` includes:

- **Custom Colors**: 
  - `primary`: #54C4C7
  - `primary-dark`: #2d8f92
  - `bg-light`: #efeadd

- **Custom Components**:
  - `.btn-primary`, `.btn-secondary`, `.btn-ghost`
  - `.card`, `.card-hover`
  - `.badge-primary`, `.badge-gray`
  - `.input-field`
  - `.gradient-text`

- **Custom Animations**:
  - `animate-fade-in-up`
  - `animate-slide-in-left`
  - `animate-pulse-glow`

## Troubleshooting

### CSS not updating?
1. Rebuild Tailwind: `./build-tailwind.sh`
2. Clear browser cache (Ctrl+Shift+R)
3. Restart Django server

### Missing classes?
- Ensure your HTML templates are in the `content` paths in `tailwind.config.js`
- Rebuild Tailwind CSS

### Node.js errors?
- Run `npm install` in the `theme/` directory
- Ensure Node.js v14+ is installed: `node --version`
