# Generated by Django 4.2.1 on 2023-06-20 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0038_alter_message_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeToSend', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('chatToSend', models.IntegerField()),
                ('typeId', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='message',
            name='time',
            field=models.CharField(default=1687288919.6347108, max_length=100),
        ),
    ]
