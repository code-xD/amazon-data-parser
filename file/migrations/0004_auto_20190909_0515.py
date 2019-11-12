# Generated by Django 2.1 on 2019-09-09 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0003_dataset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='ml_file',
            field=models.FileField(blank=True, null=True, upload_to='machinelearned'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='scraped_file',
            field=models.FileField(blank=True, null=True, upload_to='scraped'),
        ),
    ]