# Generated by Django 4.1.3 on 2022-11-15 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_alter_requests_requested_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='requests',
            name='remark',
            field=models.CharField(default='Send this much of amount', max_length=1024),
        ),
    ]
