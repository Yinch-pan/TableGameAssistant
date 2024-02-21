# Generated by Django 4.2.10 on 2024-02-19 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgs', '0005_remove_tmp_role_table_role_tmp_role_table_roleid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='role_set_table',
            name='introduction',
            field=models.CharField(blank=True, default='None', max_length=256, null=True, verbose_name='简介'),
        ),
        migrations.AlterField(
            model_name='role_table',
            name='rolename',
            field=models.CharField(blank=True, default='None', max_length=32, null=True, unique=True, verbose_name='武将名称'),
        ),
    ]