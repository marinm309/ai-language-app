# Generated by Django 5.0.7 on 2024-07-29 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='username',
        ),
        migrations.AddField(
            model_name='appuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
