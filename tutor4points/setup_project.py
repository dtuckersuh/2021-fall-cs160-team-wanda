import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tutor4points.settings')

import django
django.setup()

from django.contrib.auth import get_user_model
from core.models import School


def projectSetup():

    #add schools to School db
    if not School.objects.filter(name="San Jose State University"):
        School.objects.create(name="San Jose State University")
        print ("Added San Jose State University to School model")

    if not School.objects.filter(name="De Anza College"):
        School.objects.create(name="De Anza College")
        print ("Added De Anza College to School model")

    if not School.objects.filter(name="UC Berkeley"):
        School.objects.create(name="UC Berkeley")
        print ("Added UC Berkeley to School model")

    User = get_user_model()

    #add superuser
    if not User.objects.filter(username="admin"):
        User.objects.create_superuser(
            'admin', 'admin@gmail.com', 'wanda', school=School.objects.get(name="San Jose State University"))
        print ("Added admin (with superuser rights) to User model")

    #add tutors and tutees to Users model

    #CS sjsu student
    if not User.objects.filter(username="alexis"):
        User.objects.create_user (username="alexis", password="ad!654321", first_name="alexis", last_name="davis", email="alexis@gmail.com", school = School.objects.get(name="San Jose State University"), profile_pic="images/profile_pics/alexis.png",
        is_tutor = True, classes_taken = "CS146, MATH42, BIOL10", times_available = "Monday 2-4pm, Tuesday 5-6pm", 
        time_zone="pacific", rate = "20000")
        print ("Added Alexis Davis to Users model")

    #Art sjsu student
    if not User.objects.filter(username="amy"):
        User.objects.create_user (username="amy", password="an!654321", first_name="amy", last_name="nguyen", email="amy@gmail.com", school = School.objects.get(name="San Jose State University"), profile_pic="images/profile_pics/amy.png",
        is_tutor = True, classes_taken = "ART68, PHOT40", times_available = "Friday 1-7pm", 
        time_zone="pacific", rate = "18000")
        print ("Added Amy Nguyen to Users model")

    #Engineering sjsu student who doesn't supply rate and times available
    if not User.objects.filter(username="anthony"):
        User.objects.create_user (username="anthony", password="aj!654321", first_name="anthony", last_name="johnson", email="anthony@gmail.com", school = School.objects.get(name="San Jose State University"), profile_pic="images/profile_pics/anthony.png",
        is_tutor = True, classes_taken = "CMPE120, EE97, EE98, CMPE148", time_zone="central")
        print ("Added Anthony Johnson to Users model")

    #Medical sjsu student who does not want to be a tutor
    if not User.objects.filter(username="brandon"):
        User.objects.create_user (username="brandon", password="bc!654321", first_name="brandon", last_name="castro", email="brandon@gmail.com", school = School.objects.get(name="San Jose State University"), profile_pic="images/profile_pics/brandon.png",
        is_tutor = False, time_zone="mountain")
        print ("Added Brandon Castro to Users model")

    #Eng Berkeley student who leaves all tutor fields blank
    if not User.objects.filter(username="joshua"):
        User.objects.create_user (username="joshua", password="jc!654321", first_name="joshua", last_name="cook", email="joshua@gmail.com", school = School.objects.get(name="UC Berkeley"), profile_pic="images/profile_pics/joshua.png",
        is_tutor = True, time_zone="eastern")
        print ("Added Joshua Cook to Users model")

    #Berkeley student who does not want to be a tutor
    if not User.objects.filter(username="justin"):
        User.objects.create_user (username="justin", password="jf!654321", first_name="justin", last_name="fox", email="justin@gmail.com", school = School.objects.get(name="UC Berkeley"), profile_pic="images/profile_pics/justin.png",
        is_tutor = False, time_zone="pacific")
        print ("Added Justin Fox to Users model")

    #Music student from De Anza College who wants to be a tutor
    if not User.objects.filter(username="rui"):
        User.objects.create_user (username="rui", password="rz!654321", first_name="rui", last_name="zhao", email="rui@gmail.com", school = School.objects.get(name="De Anza College"), profile_pic="images/profile_pics/rui.png",
        is_tutor = True, classes_taken = "MUSI1A, MUSI9A, MUSI9B", times_available="Monday 12pm-8pm, Wednesday 5-8pm", time_zone="mountain")
        print ("Added Rui Zhao to Users model")
    
    #Business major student from De Anza College who wants to be a tutor
    if not User.objects.filter(username="vineeta"):
        User.objects.create_user (username="vineeta", password="vs!654321", first_name="vineeta", last_name="singh", email="vineeta@gmail.com", school = School.objects.get(name="De Anza College"), profile_pic="images/profile_pics/vineeta.png",
        is_tutor = True, classes_taken = "BUS10, CIS3, ACCT1A, ACCT1B", times_available="Monday 12pm-8pm, Wednesday 5-8pm", time_zone="mountain")
        print ("Added Vineeta Singh to Users model")

if __name__ == '__main__':
    projectSetup()
    print("Done")
