#wsgi.py
"""
WSGI config — required for deployment.
Not heavily used in local development, but included for completeness.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_analyzer.settings")
application = get_wsgi_application()
