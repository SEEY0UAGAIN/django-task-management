# Generated by Django 5.0.4 on 2024-06-10 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0025_group_leader_group_members_alter_member_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_leader',
            field=models.BooleanField(default=False),
        ),
    ]
