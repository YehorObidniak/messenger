# Generated by Django 4.2.1 on 2023-06-02 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0026_message_departmentname_alter_chat_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='department',
        ),
    ]