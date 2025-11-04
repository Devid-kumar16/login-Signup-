import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loginSignup.settings')
django.setup()

c = Client()
for path in ['/', '/signup/', '/accounts/login/']:
    # provide a Host header Django will accept in local dev
    resp = c.get(path, HTTP_HOST='127.0.0.1')
    print(path, resp.status_code)
    if resp.status_code != 200:
        # print some info to help debug
        print('Templates used:', getattr(resp, 'templates', None))
        print('Content (first 300 chars):', resp.content[:300])
    else:
        print('Templates used (repr):', [repr(t) for t in resp.templates])

# Also try to load specific templates by name
from django.template import loader
for name in ['home.html', 'registration/signup.html', 'registration/login.html']:
    try:
        tpl = loader.get_template(name)
        print('Loaded template:', name, '->', tpl)
    except Exception as e:
        print('Failed to load template', name, '->', e)
