# Generated by Django 4.2.16 on 2024-12-05 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0016_contactmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactmessage',
            name='created_at',
        ),
    ]
