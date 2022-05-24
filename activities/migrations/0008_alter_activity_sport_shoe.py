# Generated by Django 4.0.4 on 2022-05-24 12:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0007_activity_sport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='sport',
            field=models.CharField(choices=[('running', 'Running'), ('hiking', 'Hiking')], default='running', max_length=64),
        ),
        migrations.CreateModel(
            name='Shoe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('manufacturer', models.CharField(max_length=255)),
                ('brand', models.CharField(max_length=255)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
