# Generated by Django 2.2 on 2020-11-08 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201103_1746'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='family_name',
            new_name='last_name',
        ),
    ]