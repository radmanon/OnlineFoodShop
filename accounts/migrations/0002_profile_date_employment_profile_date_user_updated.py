# Generated by Django 4.1 on 2022-09-25 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date_employment',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='date_user_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
