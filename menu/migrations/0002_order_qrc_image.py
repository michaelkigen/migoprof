# Generated by Django 4.2.1 on 2023-07-09 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='qrc_image',
            field=models.ImageField(null=True, upload_to='qr_code_images'),
        ),
    ]
