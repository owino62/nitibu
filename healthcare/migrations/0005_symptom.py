# Generated by Django 4.2.16 on 2024-11-22 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0004_remove_typhoidphoto_ugonjwa_typhoid_typhoi_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('desc', models.TextField()),
            ],
        ),
    ]