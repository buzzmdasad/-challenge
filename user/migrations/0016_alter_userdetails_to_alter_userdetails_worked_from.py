# Generated by Django 5.0.7 on 2024-08-29 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_alter_userdetails_to_alter_userdetails_worked_from'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='to',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='worked_from',
            field=models.DateField(default=None, null=True),
        ),
    ]
