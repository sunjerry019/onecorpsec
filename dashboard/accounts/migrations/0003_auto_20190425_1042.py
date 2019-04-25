# Generated by Django 2.2 on 2019-04-25 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190425_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='databaseuser',
            name='reply_to',
            field=models.EmailField(blank=True, help_text='Email that people can choose to reply to for any information emails, if different from email', max_length=254, verbose_name='reply_to'),
        ),
    ]