# Generated by Django 3.1.1 on 2020-09-12 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0020_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='filmweb_score',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]