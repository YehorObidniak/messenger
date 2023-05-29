# Generated by Django 4.2.1 on 2023-05-24 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0012_rename_username_users_name_remove_users_department_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='users',
        ),
        migrations.AddField(
            model_name='users',
            name='depatment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chats.department'),
        ),
    ]