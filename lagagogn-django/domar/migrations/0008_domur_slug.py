# Generated by Django 2.1.4 on 2018-12-04 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domar', '0007_auto_20181128_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='domur',
            name='slug',
            field=models.SlugField(default='', max_length=100),
        ),
    ]
