# Generated by Django 2.1.3 on 2018-11-23 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domar', '0004_domur_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domur',
            name='appellants',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='domur',
            name='parties',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='domur',
            name='plaintiffs',
            field=models.TextField(blank=True),
        ),
    ]