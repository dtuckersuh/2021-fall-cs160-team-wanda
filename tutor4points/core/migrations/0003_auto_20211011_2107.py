# Generated by Django 3.2.6 on 2021-10-11 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20211006_0609'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='average_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, default='images/profile_pics/default_pic.png', upload_to='images/profile_pics'),
        ),
    ]