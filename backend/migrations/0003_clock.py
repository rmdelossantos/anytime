# Generated by Django 2.2.1 on 2022-07-22 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_user_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clocked_in', models.DateTimeField()),
                ('clocked_out', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_clock', to='backend.User')),
            ],
        ),
    ]