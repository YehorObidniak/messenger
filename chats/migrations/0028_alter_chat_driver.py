# Generated by Django 4.2.1 on 2023-06-05 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0027_remove_chat_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chats.driver', unique=True),
        ),
    ]
