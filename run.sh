#!/bin/bash

# Modern Blog Site - Development Server Startup Script

cd /home/ubuntu/Desktop/projects/modern-block-site

# Activate virtual environment
source venv/bin/activate

# Set admin password
export DJANGO_SUPERUSER_PASSWORD='admin123'

# Apply migrations
python manage.py migrate

# Create superuser if it doesn't exist
python manage.py shell << END
from django.contrib.auth.models import User

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Superuser 'admin' created successfully!")
else:
    print("ℹ️  Superuser 'admin' already exists")

# Create staff user
if not User.objects.filter(username='staff').exists():
    staff_user = User.objects.create_user('staff', 'staff@example.com', 'staff123')
    staff_user.is_staff = True
    staff_user.save()
    print("✅ Staff user 'staff' created successfully!")
else:
    print("ℹ️  Staff user 'staff' already exists")
END

# Collect static files
python manage.py collectstatic --noinput

# Start the development server
echo ""
echo "=============================================="
echo "🚀 Modern Blog Starting..."
echo "=============================================="
echo ""
echo "Admin Panel: http://localhost:8000/admin/"
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "Blog Site: http://localhost:8000/"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=============================================="
echo ""

python manage.py runserver 0.0.0.0:8000
