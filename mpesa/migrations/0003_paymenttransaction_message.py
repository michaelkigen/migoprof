# Generated by Django 4.2.1 on 2023-07-07 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa', '0002_remove_paymenttransaction_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenttransaction',
            name='message',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
