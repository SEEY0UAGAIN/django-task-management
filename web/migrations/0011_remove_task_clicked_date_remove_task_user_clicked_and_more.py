# Generated by Django 5.0.4 on 2024-05-11 12:43

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_task_clicked_date_task_user_clicked_alter_task_id_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='clicked_date',
        ),
        migrations.RemoveField(
            model_name='task',
            name='user_clicked',
        ),
        migrations.CreateModel(
            name='ClickHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clicked_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
