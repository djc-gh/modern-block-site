# 🎨 Modern Blog Site - Configuration & Customization Guide

## 🎯 Initial Setup Checklist

After installation, follow these steps:

### 1. Security Configuration
```bash
# Generate a new SECRET_KEY for production
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

Update `.env`:
```env
SECRET_KEY=<your-generated-key>
DEBUG=False  # In production
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 2. Create Categories
1. Go to `/admin/blog/category/`
2. Add these categories (or your own):
   - Technology
   - Lifestyle
   - Business
   - Travel
   - Food

### 3. Create First Post
1. Go to `/admin/blog/post/`
2. Click "Add Post"
3. Fill in:
   - Title: "Welcome to Modern Blog"
   - Excerpt: "This is our first blog post"
   - Content: Write your content
   - Category: Select one
   - Featured Image: Upload an image
   - Status: Published
   - Featured: Check if you want it on homepage
4. Save

## 🎨 Branding & Colors

### Change Primary Colors

#### Option 1: Update Settings
Edit `config/settings.py`:
```python
# Add custom settings for colors
PRIMARY_COLOR = '#54C4C7'
PRIMARY_DARK = '#2d8f92'
BG_COLOR = '#efeadd'
```

#### Option 2: Update Tailwind Config
Edit `tailwind.config.js`:
```javascript
theme: {
    extend: {
        colors: {
            primary: '#YOUR_COLOR',
            'primary-dark': '#YOUR_DARK_COLOR',
            'bg-light': '#YOUR_BG_COLOR',
        }
    }
}
```

#### Option 3: Update Base Template
Edit `templates/base.html`:
```css
:root {
    --primary: #YOUR_COLOR;
    --primary-dark: #YOUR_DARK_COLOR;
    --bg-light: #YOUR_BG_COLOR;
}
```

### Add Your Logo

1. Place logo file in `static/images/logo.png`
2. Update `templates/partials/navbar.html`:
```html
<img src="{% static 'images/logo.png' %}" alt="Logo" class="h-10">
```

### Change Site Name

Edit `config/settings.py`:
```python
SITE_NAME = "Your Blog Name"
```

Edit `config/urls.py`:
```python
admin.site.site_header = "Your Blog Admin"
admin.site.site_title = "Your Blog"
```

## 📱 Template Customization

### Homepage Banner
Edit `templates/blog/post_list.html`:
```html
<h1 class="text-4xl md:text-5xl font-bold mb-4">
    Your Custom Title
</h1>
<p class="text-lg md:text-xl text-white/90">
    Your custom subtitle
</p>
```

### Footer Links
Edit `templates/partials/footer.html`:
- Update social media links
- Change company info
- Add custom pages

### Navbar Menu
Edit `templates/partials/navbar.html`:
- Add/remove navigation items
- Customize menu items
- Add dropdowns

## 🔐 User Management

### Create Additional Admins
```bash
python manage.py createsuperuser
```

Follow the prompts to create a new admin user.

### Grant Admin Permissions
In Django admin:
1. Go to Users
2. Select a user
3. Check "Staff status"
4. Check "Superuser status"
5. Save

## 📧 Email Configuration

### Configure Email Backend
Edit `config/settings.py`:

#### For Gmail:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

#### For SendGrid:
```python
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = 'your-sendgrid-api-key'
```

#### For Console (Development):
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## 🗄️ Database Configuration

### SQLite (Default - Development)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### PostgreSQL (Recommended - Production)

1. Install PostgreSQL
2. Create database: `createdb modernblog`
3. Install psycopg2: `pip install psycopg2-binary`
4. Update `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'modernblog',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. Run migrations: `python manage.py migrate`

### MySQL
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'modernblog',
        'USER': 'root',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## 🖼️ Media Files & Image Processing

### Configure Media Directory
Already configured in `config/settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Image Optimization (Optional)
Install Pillow (already included):
```bash
pip install Pillow
```

### Serving Media Files
In development (already configured in `urls.py`):
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

For production, use a CDN like AWS S3, Cloudinary, or Bunny CDN.

## 🔍 SEO Configuration

### Add Meta Tags to Posts
Edit `models.py` and add:
```python
meta_description = models.CharField(max_length=160)
meta_keywords = models.CharField(max_length=255)
```

### Update Templates
Edit `templates/blog/post_detail.html`:
```html
{% block meta_description %}{{ post.meta_description }}{% endblock %}
```

### Generate Sitemaps
Create `apps/blog/sitemaps.py`:
```python
from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, item):
        return item.updated_at
```

## 💾 Backup & Maintenance

### Database Backup
```bash
# SQLite
cp db.sqlite3 db.sqlite3.backup

# PostgreSQL
pg_dump modernblog > backup.sql
```

### Static Files
```bash
python manage.py collectstatic
```

### Regular Maintenance
```bash
# Check for issues
python manage.py check

# Update dependencies
pip install --upgrade -r requirements.txt

# Run migrations
python manage.py migrate
```

## 🚀 Performance Optimization

### Enable Caching
Edit `config/settings.py`:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Compress Static Files
```bash
pip install django-compressor
```

Edit `config/settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'compressor',
]

COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinCompressor',
]
```

### Database Optimization
- Use `select_related()` for ForeignKeys
- Use `prefetch_related()` for reverse relations
- Add database indexes
- Paginate large querysets

## 🔒 Security Hardening

### Update Security Settings
```python
# Security middleware
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
]

# Session security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
```

### Rate Limiting
Install django-ratelimit:
```bash
pip install django-ratelimit
```

## 📱 Mobile App Considerations

### PWA (Progressive Web App)
Add `manifest.json` to `static/`:
```json
{
  "name": "Modern Blog",
  "short_name": "Blog",
  "icons": [{
    "src": "/static/images/icon-192.png",
    "sizes": "192x192",
    "type": "image/png"
  }],
  "theme_color": "#54C4C7",
  "background_color": "#efeadd"
}
```

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Create Test Cases
Create `apps/blog/tests.py`:
```python
from django.test import TestCase
from .models import Post, Category

class PostModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test')
        
    def test_post_creation(self):
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            category=self.category
        )
        self.assertEqual(str(post), 'Test Post')
```

## 🐛 Debugging

### Debug Toolbar
Install django-debug-toolbar:
```bash
pip install django-debug-toolbar
```

Add to `INSTALLED_APPS` and `MIDDLEWARE`.

### Logging
Configure logging in `config/settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
```

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/misc/design-philosophies/)
- [Web.dev Performance](https://web.dev/)

---

**Need help? Check README.md for full documentation!**
