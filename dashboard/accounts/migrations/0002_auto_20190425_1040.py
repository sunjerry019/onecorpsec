# Generated by Django 2.2 on 2019-04-25 02:40

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='databaseuser',
            managers=[
                ('objects', accounts.models.DatabaseUserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='databaseuser',
            name='reply_to',
            field=models.CharField(blank=True, help_text='Email that people can choose to reply to for any information emails, if different from email', max_length=254, verbose_name='reply_to'),
        ),
    ]