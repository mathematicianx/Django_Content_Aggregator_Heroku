# Generated by Django 3.1.1 on 2020-09-09 18:17

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0014_auto_20200909_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simplead',
            name='body',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='simplead',
            name='slug',
            field=models.SlugField(max_length=250, unique_for_date=models.DateTimeField(auto_now_add=True)),
        ),
    ]