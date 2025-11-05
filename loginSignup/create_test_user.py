import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loginSignup.settings')
django.setup()
from django.contrib.auth.models import User

username = 'testuser'
password = 'TestPass123!'
email = 'testuser@example.com'

if User.objects.filter(username=username).exists():
    print('User already exists:', username)
else:
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    print('Created user:', username, 'password:', password)

# Print summary
print('Total users:', User.objects.count())
for u in User.objects.all():
    print(u.id, u.username, u.email, 'date_joined=', u.date_joined, 'last_login=', u.last_login)
