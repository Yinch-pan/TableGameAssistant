from django.db import models


# Create your models here.


class Country_Table(models.Model):
    country = models.CharField(max_length=32, unique=True, null=True, blank=True, default='None', verbose_name='势力')


class Role_Table(models.Model):
    rolename = models.CharField(unique=True,max_length=32, null=True, blank=True, default='None', verbose_name='武将名称')
    # rolecountry = models.ForeignKey(to='Country_Table',to_field='country',on_delete=models.CASCADE)


class Role_Set_Table(models.Model):
    setname = models.CharField(max_length=32, null=True, blank=True, default='None', verbose_name='武将名称')
class Tmp_Role_Table(models.Model):
     rolename=models.ForeignKey(to=Role_Table,to_field='rolename',on_delete=models.CASCADE)


class Roleset_Detail_Table(models.Model):
    roleid=models.ForeignKey(to=Role_Table,to_field='id',on_delete=models.CASCADE)
    setid=models.ForeignKey(to=Role_Set_Table,to_field='id',on_delete=models.CASCADE)

