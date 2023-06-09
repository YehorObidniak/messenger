# Generated by Django 4.2.1 on 2023-05-22 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0006_remove_message_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=64, unique=True)),
                ('password', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=64)),
                ('department', models.CharField(max_length=64)),
                ('isManager', models.BooleanField(default=False)),
            ],
        ),
    ]
