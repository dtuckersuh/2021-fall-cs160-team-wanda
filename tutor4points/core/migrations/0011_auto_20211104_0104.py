# Generated by Django 3.2.6 on 2021-11-04 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_transaction_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor_request',
            name='tutee_comment',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='tutor_request',
            name='tutor_comment',
            field=models.TextField(null=True),
        ),
    ]
