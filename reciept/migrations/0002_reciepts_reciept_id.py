# Generated by Django 4.2.1 on 2023-08-14 05:25

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('reciept', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reciepts',
            name='reciept_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
