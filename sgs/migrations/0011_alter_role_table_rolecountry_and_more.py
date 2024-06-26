# Generated by Django 4.2.10 on 2024-05-13 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgs', '0010_role_table_rolecountry_role_table_rolegender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role_table',
            name='rolecountry',
            field=models.CharField(blank=True, default='None', max_length=32, null=True, verbose_name='势力'),
        ),
        migrations.AlterField(
            model_name='role_table',
            name='rolegender',
            field=models.CharField(blank=True, default='None', max_length=32, null=True, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='role_table',
            name='rolename',
            field=models.CharField(blank=True, default='None', max_length=32, null=True, verbose_name='武将名称'),
        ),
        migrations.AlterField(
            model_name='role_table',
            name='roleserver',
            field=models.CharField(blank=True, default='None', max_length=32, null=True, verbose_name='服务器'),
        ),
    ]
