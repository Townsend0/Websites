# Generated by Django 4.2.2 on 2023-06-17 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roxy', '0009_alter_card_facebook_alter_card_twitter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='content',
            field=models.TextField(max_length=250),
        ),
    ]
