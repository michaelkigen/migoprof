# Generated by Django 4.2.1 on 2023-07-26 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='points',
            field=models.DecimalField(decimal_places=1, default=1, max_digits=6),
        ),
    ]
