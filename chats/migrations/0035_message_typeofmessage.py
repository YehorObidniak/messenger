# Generated by Django 4.2.1 on 2023-06-19 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0034_message_audioname'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='typeOfMessage',
            field=models.CharField(choices=[('photo', 'photo'), ('text', 'text'), ('audio', 'audio'), ('video', 'video')], default='text', max_length=25),
        ),
    ]
