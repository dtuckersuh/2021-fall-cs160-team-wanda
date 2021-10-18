# Generated by Django 3.2.6 on 2021-10-15 02:22

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20211012_0426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.school'),
        ),
        migrations.CreateModel(
            name='tutor_request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=100)),
                ('date_requested', models.DateField(auto_now=True)),
                ('tutor_date', models.DateField()),
                ('location', models.CharField(max_length=100)),
                ('time', models.TimeField()),
                ('accepted', models.BooleanField(null=True)),
                ('completed', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('tutee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('tutor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tutor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.FloatField()),
                ('method', models.CharField(choices=[('visa', 'VISA'), ('points', 'POINTS')], max_length=25)),
                ('date', models.DateField()),
                ('sent_from', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_from', to=settings.AUTH_USER_MODEL)),
                ('sent_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('tutee', 'TUTEE'), ('tutor', 'TUTOR')], max_length=5)),
                ('rating', models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('date', models.DateField(auto_now=True)),
                ('comment', models.TextField()),
                ('given_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='given_by', to=settings.AUTH_USER_MODEL)),
                ('given_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]