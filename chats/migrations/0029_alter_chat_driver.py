# Generated by Django 4.2.1 on 2023-06-05 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0028_alter_chat_driver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='driver',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='chats.driver'),
        ),
    ]
