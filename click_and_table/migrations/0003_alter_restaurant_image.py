# Generated by Django 3.2.2 on 2021-05-24 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('click_and_table', '0002_auto_20210524_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
