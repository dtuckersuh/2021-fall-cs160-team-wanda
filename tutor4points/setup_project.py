import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutor4points.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
from core.models import School


def projectSetup():

    if not School.objects.filter(name="San Jose State University"):
        school1 = School(name="San Jose State University")
        school1.save()

    if not School.objects.filter(name="De Anza College"):
        school2 = School(name="De Anza College")
        school2.save()

    if not School.objects.filter(name="UC Berkeley"):
        school3 = School(name="UC Berkeley")
        school3.save()

    User = get_user_model()

    if not User.objects.filter(username="admin"):
        User.objects.create_superuser(
            'admin', 'admin@gmail.com', 'wanda', school=school1)


if __name__ == '__main__':
    projectSetup()
    print("Done")
