import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meektech.settings')
import django
django.setup()

from django.contrib.admin.models import LogEntry

def main():
    qs = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:20]
    print('LogEntry count:', LogEntry.objects.count())
    if not qs:
        print('No recent LogEntry rows found.')
        return
    for e in qs:
        user = e.user.username if e.user else 'system'
        print(f"{e.action_time} | {user} | {e.get_change_message()} | {e.object_repr} | {e.action_flag}")

if __name__ == '__main__':
    main()
