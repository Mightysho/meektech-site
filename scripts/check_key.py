import os
import sys
# Ensure project root is on sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meektech.settings')
try:
    import django
    django.setup()
    from django.conf import settings
    k = getattr(settings, 'GOOGLE_MAPS_API_KEY', None)
    print('KEY_PRESENT' if k else 'KEY_MISSING')
    if k:
        print('MASKED:' + (k[:4] + '...' + k[-4:]))
except Exception as e:
    print('ERROR:', e)
    sys.exit(1)
