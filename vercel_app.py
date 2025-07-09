import os
import sys
from django.core.wsgi import get_wsgi_application
from django.core.management import execute_from_command_line

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celio.settings')

# Collect static files on startup (commented out for debugging)
# try:
#     execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--clear'])
# except Exception as e:
#     print(f"Static files collection failed: {e}")

# Get the WSGI application
application = get_wsgi_application()

# Vercel handler
app = application