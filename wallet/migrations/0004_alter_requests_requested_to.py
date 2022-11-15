# Generated by Django 4.1.3 on 2022-11-14 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('wallet', '0003_rename_requested_user_requests_requested_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='requested_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_requests', to='authentication.users'),
        ),
    ]