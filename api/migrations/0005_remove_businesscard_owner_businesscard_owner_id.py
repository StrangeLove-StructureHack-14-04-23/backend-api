# Generated by Django 4.0.5 on 2023-04-15 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_businesscard_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businesscard',
            name='owner',
        ),
        migrations.AddField(
            model_name='businesscard',
            name='owner_id',
            field=models.IntegerField(null=True, verbose_name='Айди создателя'),
        ),
    ]
