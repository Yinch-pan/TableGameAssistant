import random

from django.shortcuts import render, redirect
from sgs import models


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
    if request.method == 'GET':
        search = request.GET.get('searchrole')
        if search is None:
            search = ''
        allrole = models.Role_Table.objects.exclude(
            tmp_role_table__in=models.Tmp_Role_Table.objects.values('id')).filter(rolename__icontains=search).all()
        tmpset = models.Role_Table.objects.filter(tmp_role_table__in=models.Tmp_Role_Table.objects.values('id')).all()

        return render(request, 'addroleset.html', {'allrole': allrole, 'tmpset': tmpset, 'searchrole': search})

    setname = request.POST.get('rolesetname')
    setintro = request.POST.get('introductionTextarea')

    models.Set_Table.objects.create(setname=setname, introduction=setintro)

    setid = models.Set_Table.objects.filter(setname=setname).first().id

    for obj in models.Tmp_Role_Table.objects.all():
        models.Roleset_Detail_Table.objects.create(setid_id=setid, roleid_id=obj.roleid_id)

    models.Tmp_Role_Table.objects.all().delete()
    return redirect('/sgs/addset')


def deltmprole(request):
    rolename = request.GET.get('rolename')
    search = request.GET.get('searchrole')
    models.Tmp_Role_Table.objects.filter(roleid_id=rolename).delete()
    return redirect(f'/sgs/addset?searchrole={search}')


def addtmprole(request):
    rolename = request.GET.get('rolename')
    search = request.GET.get('searchrole')
    models.Tmp_Role_Table.objects.create(roleid_id=rolename)
    return redirect(f'/sgs/addset?searchrole={search}')


def addsetrole(request):
    roleid = request.GET.get('roleid')
    setid = request.GET.get('setid')
    models.Roleset_Detail_Table.objects.create(roleid_id=roleid, setid_id=setid)
    search = request.GET.get('searchrole')
    if search is None:
        search = ''
    return redirect(f'/sgs/editroleset?rolesetid={setid}&searchrole={search}')


def delsetrole(request):
    roleid = request.GET.get('roleid')
    setid = request.GET.get('setid')

    models.Roleset_Detail_Table.objects.filter(roleid_id=roleid, setid_id=setid).delete()
    search = request.GET.get('searchrole')
    if search is None:
        search = ''
    return redirect(f'/sgs/editroleset?rolesetid={setid}&searchrole={search}')


def roleset(request):
    allset = models.Set_Table.objects.all()
    return render(request, 'roleset.html', {'allset': allset})


def delset(request):
    setid = request.GET.get('setid')
    models.Set_Table.objects.filter(id=setid).delete()
    return redirect('/sgs/roleset')

def randroleset(request):
    setid=request.GET.get('rolesetid')
    num=int(request.GET.get('randnum'))
    allrole=models.Roleset_Detail_Table.objects.filter(setid=setid).order_by('?').all()
    setdata=models.Set_Table.objects.filter(id=setid).first()

    print(allrole)
    allrole=models.Role_Table.objects.filter(id__in=allrole[:num].values('roleid_id')).all()
    return render(request,'randroleset.html',{'setdata':setdata,'allrole':allrole,'randnum':num})


def editroleset(request):


    rolesetid = request.GET.get('rolesetid')
    roleidinset = models.Roleset_Detail_Table.objects.filter(setid_id=rolesetid).all()
    roleinset = models.Role_Table.objects.filter(id__in=roleidinset.values('roleid_id'))
    rolenotinset = models.Role_Table.objects.exclude(id__in=roleidinset.values('roleid_id'))

    if request.method == 'POST':
        intro = request.POST.get('introductionTextarea')

        models.Set_Table.objects.filter(id=rolesetid).update(introduction=intro)

    search = request.GET.get('searchrole')
    if search is None:
        search = ''
    rolenotinset = rolenotinset.filter(rolename__icontains=search)
    setdata = models.Set_Table.objects.filter(id=rolesetid).first()

    return render(request, 'editroleset.html',
                  {'roleinset': roleinset, 'rolenotinset': rolenotinset, 'setdata': setdata, 'searchrole': search})

def faceas(request):
    return render(request,'faceas.html')

def cardrecord(request):
    return render(request,'cardrecord.html')

def cardrecords(request):
    return render(request,'cardrecords.html')

def randomnum(request):
    return render(request,'randomnum.html')


def playersit(request):
    return render(request,'playersit.html')

