# Generated by Django 4.2.1 on 2023-06-19 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0035_message_typeofmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='audioName',
        ),
    ]
