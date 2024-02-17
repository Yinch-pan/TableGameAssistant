from django.db import models


# Create your models here.


class Country_Table(models.Model):
    country = models.CharField(max_length=32,unique=True, null=True, blank=True, default='None', verbose_name='势力')


class Role_Table(models.Model):
    rolename = models.CharField(max_length=32, null=True, blank=True, default='None', verbose_name='武将名称')
    # rolecountry = models.ForeignKey(to='Country_Table',to_field='country',on_delete=models.CASCADE)


