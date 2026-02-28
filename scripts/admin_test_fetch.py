import os
import django
import sys
import requests
import re
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meektech.settings')
try:
    # Ensure project root is on sys.path so Django can import the settings package
    project_root = str(Path(__file__).resolve().parent.parent)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    django.setup()
except Exception as e:
    print('Django setup error:', e)
    sys.exit(1)

from django.contrib.auth import get_user_model
User = get_user_model()
username = 'devtest'
password = 'DevTestPass123!'
email = 'devtest@example.com'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print('Created superuser', username)
else:
    print('Superuser exists')

# Now perform login via requests
session = requests.Session()
base = 'http://127.0.0.1:8000'
login_url = base + '/admin/login/'
index_url = base + '/admin/'

# Get login page
r = session.get(login_url)
if r.status_code != 200:
    print('Failed to load login page:', r.status_code)
    sys.exit(1)

# Parse csrf token
# Try to extract csrf token from form input; fallback to cookie
match = re.search(r"name='csrfmiddlewaretoken'\s+value='([^']+)'", r.text)
if not match:
    match = re.search(r'name="csrfmiddlewaretoken"\s+value="([^"]+)"', r.text)
if match:
    csrf = match.group(1)
else:
    csrf = session.cookies.get('csrftoken', '')

payload = {
    'username': username,
    'password': password,
    'csrfmiddlewaretoken': csrf,
    'next': '/admin/'
}
headers = {'Referer': login_url}

r2 = session.post(login_url, data=payload, headers=headers)
if r2.status_code not in (200, 302):
    print('Login POST failed:', r2.status_code)
    sys.exit(1)

# Fetch admin index
r3 = session.get(index_url)
if r3.status_code != 200:
    print('Failed to load admin index:', r3.status_code)
    sys.exit(1)
with open('scripts/admin_index_fetched.html', 'w', encoding='utf-8') as f:
    f.write(r3.text)
    print('Saved admin index to scripts/admin_index_fetched.html')

html = r3.text
idx = html.find('class="spectra-widget welcome-widget"')
if idx == -1:
    idx = html.find("class='spectra-widget welcome-widget'")
if idx == -1:
    print('Welcome widget not found in admin index HTML; full HTML length:', len(html))
    # try to locate any spectra widgets
    for m in re.finditer('spectra-widget', html):
        start = max(0, m.start()-120)
        end = min(len(html), m.end()+120)
        print('--- context for spectra-widget at', m.start())
        print(html[start:end])
    # also search for 'Hello' greeting
    for m in re.finditer('Hello', html):
        start = max(0, m.start()-60)
        end = min(len(html), m.end()+60)
        print('--- context for Hello at', m.start())
        print(html[start:end])
else:
    # find the opening '<div' before the class string
    start = html.rfind('<div', 0, idx)
    if start == -1:
        start = idx
    # naive balancing of divs to find the matching close
    pos = start
    open_count = 0
    pattern = re.compile(r'<div\b|</div>')
    for m in pattern.finditer(html, start):
        token = m.group(0)
        if token.startswith('<div'):
            open_count += 1
        else:
            open_count -= 1
        pos = m.end()
        if open_count == 0:
            break
    snippet = html[start:pos]
    print(snippet)
