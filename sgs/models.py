import time

from django.db import models


# Create your models here.


class Country_Table(models.Model):
    country = models.CharField(max_length=32, unique=True, null=True, blank=True, default='None', verbose_name='势力')


class Role_Table(models.Model):
    rolename = models.CharField(unique=True, max_length=32, null=True, blank=True, default='None',
                                verbose_name='武将名称')
    # rolecountry = models.ForeignKey(to='Country_Table',to_field='country',on_delete=models.CASCADE)


class Set_Table(models.Model):
    setname = models.CharField(max_length=32, null=True, blank=True, default='None', verbose_name='武将名称')
    introduction = models.CharField(max_length=256, null=True, blank=True, default='None', verbose_name='简介')


class Tmp_Role_Table(models.Model):
    roleid = models.ForeignKey(to=Role_Table, to_field='id', on_delete=models.CASCADE)


class Roleset_Detail_Table(models.Model):
    roleid = models.ForeignKey(to=Role_Table, to_field='id', on_delete=models.CASCADE)
    setid = models.ForeignKey(to=Set_Table, to_field='id', on_delete=models.CASCADE)


class Table_Table(models.Model):
    randseed = models.CharField(max_length=256, null=True, blank=True, default='None', verbose_name='随机种子')
    playernum = models.IntegerField(null=True, blank=True, default='None', verbose_name='玩家人数')
    player_states = models.IntegerField(null=True, blank=True, default='None', verbose_name='玩家存活情况')
