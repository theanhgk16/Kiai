# Generated by Django 3.0.5 on 2022-08-09 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20220809_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='question',
            name='created_at',
        ),
    ]
