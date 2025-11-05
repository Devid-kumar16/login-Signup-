import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loginSignup.settings')
django.setup()
from django.contrib.auth.models import User
users = User.objects.all()
print('Total users:', users.count())
for u in users:
    print(u.id, u.username, u.email, 'date_joined=', u.date_joined, 'last_login=', u.last_login)
