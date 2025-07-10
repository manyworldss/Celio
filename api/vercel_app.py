import os
import sys
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celio.settings')

# Set production environment variables if not already set
if not os.environ.get('DJANGO_DEBUG'):
    os.environ.setdefault('DJANGO_DEBUG', 'False')
if not os.environ.get('DJANGO_ALLOWED_HOSTS'):
    os.environ.setdefault('DJANGO_ALLOWED_HOSTS', '*.vercel.app')

# Collect static files on startup
try:
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--clear'])
except Exception as e:
    print(f"Static files collection failed: {e}")

# Run migrations on startup
try:
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
except Exception as e:
    print(f"Database migration failed: {e}")

# Get the WSGI application
application = get_wsgi_application()

# Vercel handler
app = application
