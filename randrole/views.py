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
    allrole = models.Role_Table.objects.all()
    tmpset = models.Tmp_Role_Table.objects.all()
    return render(request, 'addroleset.html', {'allrole': allrole, 'tmpset': tmpset})

def deltmprole(request):
    rolename = request.GET.get('rolename')
    print(rolename)
    models.Tmp_Role_Table.objects.filter(roleid=rolename).delete()
    return redirect('/sgs/addset')
def addtmprole(request):
    rolename = request.GET.get('rolename')
    print(rolename)
    for obj in models.Role_Table.objects.all():
        print(obj.id)
    models.Tmp_Role_Table.objects.create(roleid_id=rolename)
    return redirect('/sgs/addset')
