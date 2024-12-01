# Generated by Django 4.2.16 on 2024-11-24 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0009_pic_delete_ailment_delete_picha'),
    ]

    operations = [
        migrations.CreateModel(
            name='Illness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Sign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(upload_to='illness_images/')),
                ('illness', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='healthcare.illness')),
            ],
        ),
        migrations.DeleteModel(
            name='Pic',
        ),
    ]
