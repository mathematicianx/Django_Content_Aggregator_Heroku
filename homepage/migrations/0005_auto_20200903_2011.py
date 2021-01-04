# Generated by Django 2.2.4 on 2020-09-03 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0004_auto_20200903_1955'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, unique_for_month=True)),
                ('link', models.URLField()),
                ('which_site', models.CharField(choices=[('olawa24', 'Oława24'), ('tuolawa', 'TuOława')], default='tuolawa', max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='Olawa24_news',
        ),
    ]