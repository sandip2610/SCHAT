# Generated by Django 5.1.7 on 2025-03-20 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SCHAT', '0008_delete_note_delete_videocontent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caller', models.CharField(max_length=100)),
                ('receiver', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('is_video_call', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Admission',
        ),
    ]
