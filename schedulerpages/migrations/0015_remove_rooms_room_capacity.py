# Generated by Django 5.0 on 2024-02-11 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedulerpages', '0014_combinedcourseschedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rooms',
            name='room_capacity',
        ),
    ]
