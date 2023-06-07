# Generated by Django 4.2.1 on 2023-06-07 05:06

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservisasinfo', '0011_alter_automobilis_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='automobiliomodelis',
            name='car_description',
            field=tinymce.models.HTMLField(blank=True, max_length=8000, null=True, verbose_name='Description'),
        ),
    ]
