# Generated by Django 2.1.3 on 2018-11-28 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domar', '0005_auto_20181123_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='domur',
            name='judge',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
