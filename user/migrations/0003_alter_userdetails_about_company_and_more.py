# Generated by Django 5.1 on 2024-08-18 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_userdetails_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='about_company',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='company',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='designation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='experience_level',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='responsibilities',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='skills',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='worked_from',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='year_of_passing',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
