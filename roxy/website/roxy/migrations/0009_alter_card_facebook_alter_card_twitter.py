# Generated by Django 4.2.2 on 2023-06-17 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roxy', '0008_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='facebook',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='twitter',
            field=models.URLField(blank=True, null=True),
        ),
    ]
