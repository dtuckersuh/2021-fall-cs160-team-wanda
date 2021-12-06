# Generated by Django 3.2.6 on 2021-12-05 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_tutorrequest_tutee_completed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tutorrequest',
            old_name='completed',
            new_name='both_confirm_completed',
        ),
        migrations.RenameField(
            model_name='tutorrequest',
            old_name='paid',
            new_name='both_confirm_paid',
        ),
        migrations.RenameField(
            model_name='tutorrequest',
            old_name='tutee_completed',
            new_name='tutee_confirm_completed',
        ),
        migrations.AddField(
            model_name='rating',
            name='request',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.tutorrequest'),
        ),
        migrations.AddField(
            model_name='tutorrequest',
            name='tutee_confirm_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tutorrequest',
            name='tutor_confirm_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tutorrequest',
            name='tutor_confirm_paid',
            field=models.BooleanField(default=False),
        ),
    ]