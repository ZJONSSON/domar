# Generated by Django 2.1.3 on 2018-11-22 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domar', '0002_auto_20181122_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domur',
            name='identifier',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
