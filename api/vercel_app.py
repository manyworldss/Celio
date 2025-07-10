import os
import os
import sys
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

# Add the project root to the Python path
# Assuming vercel_app.py is in api/ and manage.py is in the root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# Set default Django settings module if not already set
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celio.settings')

# Set default environment variables for Vercel if not already set
os.environ.setdefault('DJANGO_DEBUG', 'False')
os.environ.setdefault('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1,*.vercel.app')

# Run Django migrations and collect static files
# These commands are typically run during deployment/startup in serverless environments
execute_from_command_line([sys.executable, 'manage.py', 'migrate', '--noinput'])
execute_from_command_line([sys.executable, 'manage.py', 'collectstatic', '--noinput'])

# Get the WSGI application for Vercel
app = get_wsgi_application()

# Vercel handler
app = application
