# Generated by Django 4.2.2 on 2023-06-17 00:11

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roxy', '0003_alter_card_img_alter_contact_email_alter_page_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(choices=[('Vintage', 'Vintage'), ('Creative', 'Creative')], max_length=50)),
                ('img', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('job', models.CharField(max_length=50)),
                ('img', models.ImageField(blank=True, default='testimonial/default', null=True, upload_to='testimonial')),
                ('testimony', ckeditor.fields.RichTextField()),
            ],
        ),
    ]
