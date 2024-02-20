from django.shortcuts import render, redirect
from randrole import models


# Create your views here.
def randomrole(request):
    return render(request, 'test.html')


def addrole(request):
    if request.method == 'GET':
        return render(request, 'addrole.html')

    dataname = request.POST.get('rolename')
    models.Role_Table.objects.create(rolename=dataname)
    return redirect('/sgs/add')


def rolenow(request):
    allrole = models.Role_Table.objects.all()
    return render(request, 'role.html', {'allrole': allrole})


def deleaterole(request):
    roleid = request.GET.get('roleid')
    models.Role_Table.objects.filter(id=roleid).delete()
    return redirect('/sgs/role')


def homepage(request):
    return render(request, 'sgshomepage.html')


def addroleset(request):
    if request.method=='GET':
        allrole = models.Role_Table.objects.exclude(tmp_role_table__in=models.Tmp_Role_Table.objects.values('id')).all()
        tmpset = models.Role_Table.objects.filter(tmp_role_table__in=models.Tmp_Role_Table.objects.values('id')).all()

        return render(request, 'addroleset.html', {'allrole': allrole, 'tmpset': tmpset})

    setname=request.POST.get('rolesetname')
    setintro=request.POST.get('introductionTextarea')
    models.Role_Set_Table.objects.create(setname=setname,introduction=setintro)

    setid=models.Role_Set_Table.objects.filter(setname=setname).first().id

    for obj in models.Tmp_Role_Table.objects.all():
        models.Roleset_Detail_Table.objects.create(setid_id=setid,roleid_id=obj.roleid_id)

    models.Tmp_Role_Table.objects.all().delete()
    return redirect('/sgs/addset')


def deltmprole(request):
    rolename = request.GET.get('rolename')
    models.Tmp_Role_Table.objects.filter(roleid_id=rolename).delete()
    return redirect('/sgs/addset')
def addtmprole(request):
    rolename = request.GET.get('rolename')
    models.Tmp_Role_Table.objects.create(roleid_id=rolename)
    return redirect('/sgs/addset')
def roleset(request):
    allset=models.Role_Set_Table.objects.all()
    return render(request,'roleset.html',{'allset':allset})
def delset(request):
    setid=request.GET.get('setid')
    models.Role_Set_Table.objects.filter(id=setid).delete()
    return redirect('/sgs/roleset')


