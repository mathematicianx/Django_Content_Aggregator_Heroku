# Generated by Django 3.1.1 on 2020-09-07 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0010_auto_20200906_1828'),
    ]

    operations = [
        migrations.AddField(
            model_name='simplead',
            name='image',
            field=models.ImageField(blank=True, upload_to='uploads/'),
        ),
    ]
