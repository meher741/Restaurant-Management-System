import os
import sys
import django
from pathlib import Path

# Set up Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Test database connection
from django.db import connection
try:
    connection.ensure_connection()
    print("Database connection successful")
except Exception as e:
    print(f"Database connection failed: {e}")
