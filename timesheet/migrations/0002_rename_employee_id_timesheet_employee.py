# Generated by Django 4.2.4 on 2023-08-24 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timesheet',
            old_name='employee_id',
            new_name='employee',
        ),
    ]
