# Generated by Django 4.2.1 on 2023-06-27 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0043_alter_message_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='time',
            field=models.CharField(default=1687874161.2542338, max_length=100),
        ),
        migrations.AlterField(
            model_name='notification',
            name='typeId',
            field=models.IntegerField(default=1),
        ),
    ]