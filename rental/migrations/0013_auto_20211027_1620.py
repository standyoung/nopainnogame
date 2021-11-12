# Generated by Django 3.1.5 on 2021-10-27 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental', '0012_rentalgame_game_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentaldevice',
            name='device_color',
        ),
        migrations.AlterField(
            model_name='rentalgame',
            name='game_video',
            field=models.URLField(blank=True, null=True),
        ),
    ]
