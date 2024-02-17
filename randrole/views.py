from django.shortcuts import render, redirect
from randrole import models


# Create your views here.
def randomrole(request):
    return render(request, 'test.html')


def addrole(request):
    if request.method=='GET':
        return render(request, 'addrole.html')

    dataname=request.POST.get('rolename')
    models.Role_Table.objects.create(rolename=dataname)
    return redirect('/sgs/add')
def rolenow(request):
    allrole = models.Role_Table.objects.all()
    return render(request, 'role.html', {'allrole': allrole})

def deleaterole(request):
    roleid=request.GET.get('roleid')
    models.Role_Table.objects.filter(id=roleid).delete()
    return redirect('/sgs/role')