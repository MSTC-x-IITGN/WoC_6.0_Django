# Generated by Django 4.1.6 on 2023-02-04 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0007_report_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='reportID',
            field=models.UUIDField(default='b41fcd6a-0c9a-4714-b63d-2caf0b56eae4'),
            preserve_default=False,
        ),
    ]