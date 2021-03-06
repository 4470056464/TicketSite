# Generated by Django 3.0.2 on 2020-01-27 06:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_auto_20200127_0927'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='code',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
