#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Create admin superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Superuser 'admin' created!")
else:
    print("ℹ️  Superuser 'admin' already exists")

# Create staff user
if not User.objects.filter(username='staff').exists():
    staff_user = User.objects.create_user('staff', 'staff@example.com', 'staff123')
    staff_user.is_staff = True
    staff_user.save()
    print("✅ Staff user 'staff' created!")
else:
    staff_user = User.objects.get(username='staff')
    staff_user.is_staff = True
    staff_user.save()
    print("ℹ️  Staff user 'staff' already exists")

print("\n" + "="*50)
print("User Accounts Created Successfully!")
print("="*50)
print("\n🔐 Superuser Account:")
print("  Username: admin")
print("  Password: admin123")
print("  Access: Full admin panel access")
print("\n👤 Staff Account:")
print("  Username: staff")
print("  Password: staff123")
print("  Access: Limited staff permissions")
print("\n" + "="*50)
