# Generated by Django 5.0.3 on 2024-03-14 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_livre_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='livre',
            name='prix',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
