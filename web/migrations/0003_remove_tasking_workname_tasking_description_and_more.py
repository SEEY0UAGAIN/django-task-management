# Generated by Django 5.0.4 on 2024-04-16 07:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20240318_2329'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasking',
            name='workname',
        ),
        migrations.AddField(
            model_name='tasking',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='tasking',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='tasking',
            name='status',
            field=models.CharField(choices=[('pending', 'กำลังดำเนินการ'), ('completed', 'สำเร็จ'), ('canceled', 'ยกเลิก')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='tasking',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='UserActivityHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(choices=[('start', 'เริ่ม'), ('complete', 'สำเร็จ'), ('cancel', 'ยกเลิก')], max_length=20)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.tasking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
