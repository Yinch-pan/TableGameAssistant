import random
import re
import time

from django.shortcuts import render, redirect
from django.db.models import Value, CharField, F
from django.db.models.functions import Concat
from sgs import models
from .get_skills import *


# Create your views here.
def randomrole(request):
    a = models.Skills_Table.objects.values_list('skill_belong', flat=True).distinct()
    models.Role_Table.objects.all().delete()
    for i in a:
        models.Role_Table.objects.create(rolename=i)
    # print(a)

    return render(request, 'test.html')


def addrole(request):
    if request.method == 'GET':
        return render(request, 'addrole.html')

    dataname = request.POST.get('rolename')
    models.Role_Table.objects.create(rolename=dataname)
    return redirect('/sgs/add')


def rolenow(request):
    result = models.Skills_Table.objects.values_list('skill_belong', 'skill_server').distinct()
    # print(result)
    # for l in result:
    #     print(l)
    # print(result)
    # for obj in result:
    # print(obj['skill_belong'])
    # tmp = models.Skills_Table.objects.filter(skill_belong=obj['skill_belong']).values('skill_server')

    # result = models.Skills_Table.objects.annotate(merged_col2=Concat('skill_server', Value(','), output_field=CharField()))
    return render(request, 'role.html', {'allrole': result})


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
    setid = request.GET.get('rolesetid')
    num = int(request.GET.get('randnum'))
    allrole = models.Roleset_Detail_Table.objects.filter(setid=setid).order_by('?').all()
    setdata = models.Set_Table.objects.filter(id=setid).first()

    allrole = models.Role_Table.objects.filter(id__in=allrole[:num].values('roleid_id')).all()
    return render(request, 'randroleset.html', {'setdata': setdata, 'allrole': allrole, 'randnum': num})


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
    return render(request, 'faceas.html')


def cardrecord(request):
    return render(request, 'cardrecord.html')


def cardrecords(request):
    return render(request, 'cardrecords.html')


def randomnum(request):
    return render(request, 'randomnum.html')


def playersit(request):
    return render(request, 'playersit.html')


def tables(request):
    all_table = models.Table_Table.objects.all()
    return render(request, 'tables.html', {"alltable": all_table})


def addtable(request):
    models.Table_Table.objects.create(randseed=None, playernum=8, player_states=255)
    tid = models.Table_Table.objects.last().id
    return redirect(f'/sgs/tables/update?tableid={tid}&player_num=8&player_states=255')


def updatetable(request):
    tableid = request.GET.get("tableid")
    playernum = request.GET.get("player_num")
    player_states = request.GET.get("player_states")
    if playernum is None: playernum = models.Table_Table.objects.filter(id=tableid).first().playernum
    if player_states is None: player_states = models.Table_Table.objects.filter(id=tableid).first().player_states
    models.Table_Table.objects.filter(id=tableid).all().update(playernum=playernum, player_states=player_states)
    player_states = int(player_states)
    playernum = int(playernum)

    player_states = int(player_states)
    lst1 = []

    for i in range(playernum):
        if ((player_states >> i) & 1) == 1:
            lst1.append(i + 1)
    lst2 = lst1.copy()
    lst3 = lst1.copy()
    if len(lst1) >= 4:
        while True:
            random.shuffle(lst1)
            random.shuffle(lst2)
            random.shuffle(lst3)
            for i in range(len(lst1)):
                if lst1[i] == lst2[i] or lst3[i] == lst2[i] or lst1[i] == lst3[i]:
                    break
            else:
                res = ' '.join([str(i) for i in lst1]) + ',' + ' '.join([str(i) for i in lst2]) + ',' + ' '.join(
                    [str(i) for i in lst3])
                models.Table_Table.objects.filter(id=tableid).all().update(randseed=res)
                break
    return redirect(f'/sgs/tables/edittable?tableid={tableid}&player_num={playernum}&player_states={player_states}')


def deltable(request):
    tableid = request.GET.get('tableid')
    models.Table_Table.objects.filter(id=tableid).all().delete()
    return redirect('/sgs/tables')


def edittable(request):
    tableid = request.GET.get("tableid")
    playernum = request.GET.get("player_num")
    player_states = request.GET.get("player_states")
    if playernum is None: playernum = models.Table_Table.objects.filter(id=tableid).first().playernum
    if player_states is None: player_states = models.Table_Table.objects.filter(id=tableid).first().player_states
    models.Table_Table.objects.filter(id=tableid).all().update(playernum=playernum, player_states=player_states)
    player_states = int(player_states)
    playernum = int(playernum)
    tabledata = models.Table_Table.objects.filter(id=tableid).first()
    rsd = models.Table_Table.objects.filter(id=tableid).first().randseed

    player_states = int(player_states)
    lst1 = []

    for i in range(playernum):
        if ((player_states >> i) & 1) == 1:
            lst1.append(i + 1)
    if len(lst1) < 4:
        lst1 = []
        lst2 = []
        lst3 = []
        return render(request, 'edittable.html', {'tabledata': tabledata, "proatk": [lst1, lst2, lst3]})
    if set(lst1) != set([int(i) for i in rsd.split(',')[0].split()]):
        return redirect(f'/sgs/tables/update?tableid={tableid}&player_num={playernum}&player_states={player_states}')

    lst1 = [int(i) for i in rsd.split(',')[0].split()]
    lst2 = [int(i) for i in rsd.split(',')[1].split()]
    lst3 = [int(i) for i in rsd.split(',')[2].split()]
    return render(request, 'edittable.html', {'tabledata': tabledata, "proatk": [lst1, lst2, lst3]})


# def roledetail(request):
#     img=open('./img/SP孙尚香.png',"rb").read()
# return render(request, 'roledetail.html')
#

def roleskills(request):
    return render(request, 'roleskills.html')


def skills(request):
    allskills = models.Skills_Table.objects.all().order_by('skill_server')
    sb = request.POST.get('sb')
    ss = request.POST.get('ss')
    st = request.POST.get('st')
    sn = request.POST.get('sn')
    sd = request.POST.get('sd')
    action = request.POST.get('btn')
    x = request.POST.get('X')
    # print(action)
    if sb is not None:
        allskills = allskills.filter(skill_belong__regex=sb).order_by().all()
    else:
        sb = ''
    if ss is not None:
        allskills = allskills.filter(skill_server__regex=ss).order_by().all()
    else:
        ss = ''
    if st is not None:
        allskills = allskills.filter(skill_type__regex=st).order_by().all()
    else:
        st = ''
    if sn is not None:
        allskills = allskills.filter(skill_name__regex=sn).order_by().all()
    else:
        sn = ''
    if sd is not None:
        allskills = allskills.filter(skill_detail__regex=sd).order_by().all()
    else:
        sd = ''

    if action == 'si':
        if x.isdigit():
            allskills = allskills.order_by('?')[:int(x)]
        return render(request, 'skills.html',
                      {"allskills": allskills, 'ss': ss, 'sb': sb, 'sn': sn, 'st': st, 'sd': sd, 'X': x})

    return render(request, 'skills.html',
                  {"allskills": allskills, 'ss': ss, 'sb': sb, 'sn': sn, 'st': st, 'sd': sd, 'X': 'X'})


def refreshskills(request):
    # models.Skills_Table.objects.all().delete()
    # thread_pool()
    # addskill=[]
    # for obj in models.Skills_Table.objects.all():
    #     tmp=models.Skills_Table.objects.filter(skill_detail=obj.skill_detail,skill_name=obj.skill_name).all()
    #     if len(tmp)!=0:
    #         new_obj=models.Skills_Table(skill_detail=obj.skill_detail,skill_type=obj.skill_type,skill_name=obj.skill_name,skill_belong=',\n'.join(list(set([k.skill_belong for k in tmp]))),skill_server=',\n'.join(list(set([k.skill_server for k in tmp]))))
    #         tmp.delete()
    #         addskill.append(new_obj)
    # for obj in addskill:
    #     obj.save()
    #
    # type = ['主公技，', '觉醒技，', '转换技，', '锁定技，', '限定技，', '宗族技，', '势力技，', '主将技，', '副将技，',
    #         '使命技，', '蓄力技，', '阵法技，']
    # for obj in models.Skills_Table.objects.all():
    #     det = obj.skill_detail
    #     types = []
    #     for j in type:
    #         if j in det:
    #             types.append(j)
    #     models.Skills_Table.objects.filter(id=obj.id).update(skill_type=''.join(types).rstrip('，'))
    return redirect('/sgs/skills')


def xushao(request):
    t = request.GET.get('tag')
    allskills = []
    if t == '1':
        allskills = models.Skills_Table.objects.filter(skill_detail__regex=".*?出牌阶段.*?(次{0,1})，.*?",
                                                       skill_type='').order_by('?').all()
        allskills = allskills.exclude(skill_detail__regex="出牌阶段[开始|结束]",
                                      skill_type='').order_by('?').all()
    if t == '2':
        allskills = models.Skills_Table.objects.filter(skill_detail__regex=".*?[^的]结束阶段，.*?",
                                                       skill_type='').order_by('?').all()
    if t == '3':
        allskills = models.Skills_Table.objects.filter(skill_detail__regex=".*?当你受到.*?伤害后.*?",
                                                       skill_type='').order_by('?').all()

    return render(request, 'xushao.html', {'allskills': allskills[:3]})


def zuxunyou(request):
    return render(request, 'zuxunyou.html')


def caoxi(request):
    return render(request, 'caoxi.html')

def shensunquan(request):
    lst=['制衡','缔盟','安恤','秉壹','慎行','兴学','安国','诫训','下书','弘援','澜疆','诱敌','观微','调度','弼政']
    lst2=['界孙权','鲁肃','步练师','顾雍','孙休','朱治','薛综','阚泽','诸葛瑾','吾彦','周鲂','潘濬','吕范','孙邵']
    allskills = models.Skills_Table.objects.filter(skill_name__in=lst,skill_belong__in=lst2,
                                                   skill_type='',skill_server='online').order_by('?').all()
    sb = request.POST.get('sb')
    ss = request.POST.get('ss')
    st = request.POST.get('st')
    sn = request.POST.get('sn')
    sd = request.POST.get('sd')
    action = request.POST.get('btn')
    x = request.POST.get('X')
    # print(action)
    if sb is not None:
        allskills = allskills.filter(skill_belong__regex=sb).order_by().all()
    else:
        sb = ''
    if ss is not None:
        allskills = allskills.filter(skill_server__regex=ss).order_by().all()
    else:
        ss = ''
    if st is not None:
        allskills = allskills.filter(skill_type__regex=st).order_by().all()
    else:
        st = ''
    if sn is not None:
        allskills = allskills.filter(skill_name__regex=sn).order_by().all()
    else:
        sn = ''
    if sd is not None:
        allskills = allskills.filter(skill_detail__regex=sd).order_by().all()
    else:
        sd = ''

    if action == 'si':
        if x.isdigit():
            allskills = allskills.order_by('?')[:int(x)]
        return render(request, 'shensunquan.html',
                      {"allskills": allskills, 'ss': ss, 'sb': sb, 'sn': sn, 'st': st, 'sd': sd, 'X': x})

    return render(request, 'shensunquan.html',
                  {"allskills": allskills, 'ss': ss, 'sb': sb, 'sn': sn, 'st': st, 'sd': sd, 'X': 'X'})


def wuyi(request):
    lst = ['肉林', '武继', '突袭', '突袭', '清侧', '图射', '纵反', '设伏', '离间', '夺锐', '止啼', '诱敌', '断发',
           '遗礼', '明策', '明策', '决堰', '怀柔', '集智', '亦算', '亦算', '激将', '化归', '献图', '献图', '天妒',
           '悯泽', '称象', '称象', '武娘', '存畏', '清谈', '权谋', '圮秩', '绡舞', '凶疑', '勇略', '散谣', '散谣',
           '义绝', '反间', '反间', '贞良', '贞良', '空城', '空城', '违忤', '违忤', '力激', '纵反', '利驭', '无双',
           '无双', '权计', '权计', '荐言', '荐言', '夺锐', '奇制', '绝策', '绝策', '奇策', '奇策', '怠宴', '饰非',
           '饰非', '肆军', '决堰', '亦算', '心幽', '修文', '狂风', '芳妒', '称象', '称象', '破锐', '破垣', '归命',
           '勇进', '征南', '颂词', '断肠', '擎北', '清谈', '奇径', '镇骨', '绡刃', '设学', '魄袭', '覆斗', '伏间',
           '伏间']
    # print(lst)

    allskills = models.Skills_Table.objects.filter(skill_name__in=lst,
                                                   skill_type='',skill_server='十周年').order_by('?').all()
    sb = request.POST.get('sb')
    ss = request.POST.get('ss')
    st = request.POST.get('st')
    sn = request.POST.get('sn')
    sd = request.POST.get('sd')
    action = request.POST.get('btn')
    x = request.POST.get('X')
    # print(action)
    if sb is not None:
        allskills = allskills.filter(skill_belong__regex=sb).order_by().all()
    else:
        sb = ''
    if ss is not None:
        allskills = allskills.filter(skill_server__regex=ss).order_by().all()
    else:
        ss = ''
    if st is not None:
        allskills = allskills.filter(skill_type__regex=st).order_by().all()
    else:
        st = ''
    if sn is not None:
        allskills = allskills.filter(skill_name__regex=sn).order_by().all()
    else:
        sn = ''
    if sd is not None:
        allskills = allskills.filter(skill_detail__regex=sd).order_by().all()
    else:
        sd = ''

    if action == 'si':
        if x.isdigit():
            allskills = allskills.order_by('?')[:int(x)]
        return render(request, 'wuyi.html',
                      {"allskills": allskills, 'ss': ss, 'sb': sb, 'sn': sn, 'st': st, 'sd': sd, 'X': x})

    return render(request, 'wuyi.html',
                  {"allskills": allskills, 'ss': ss, 'sb': sb, 'sn': sn, 'st': st, 'sd': sd, 'X': 'X'})

    # return render(request, 'wuyi.html', {'allskills': allskills})


def zhongyan(request):
    allskills = models.Skills_Table.objects.filter(skill_detail__regex="^.{0,2}出牌阶段.*?(次{0,1})，.*?",
                                                   skill_type='').order_by('?').all()
    allskills = allskills.exclude(skill_detail__regex="出牌阶段[开始|结束]",
                                                   skill_type='').order_by('?').all()


    # allskills = models.Skills_Table.objects.all()
    # allskills = allskills.filter(skill_server="十周年").order_by('?').all()
    # allskills = allskills.filter(skill_detail__regex="X").order_by('?').all()
    # allskills = allskills.filter(skill_detail__regex="弃牌阶段").order_by('?').all()
    # allskills = allskills.filter(skill_detail__regex="判定").order_by('?').all()
    # allskills = allskills.filter(skill_detail__regex="造成伤害").order_by('?').all()
    return render(request, 'zhongyan.html', {'allskills': allskills[:3]})


def role_detail(request):
    ser = request.GET.get('ser')
    name = request.GET.get('name')
    server = ''
    if ser == '十周年': server = 'sgs'
    if ser == 'online': server = 'sgsol'
    if ser == '移动版': server = 'msgs'
    return redirect(f'https://wiki.biligame.com/{server}/{name}')
def wangrong(request):
    nowv=request.GET.get('now')
    if nowv is None:
        nowv=0
    else:
        nowv=int(nowv)
    # print(nowv)
    with open('tmp.txt','r') as f:
        # print(f.readline(),'11')
        maxv=int(f.read())
    with open('tmp.txt', 'w') as f:
        f.write(str(max(maxv,nowv)))
    return render(request, 'wangrong.html',{'maxv':max(maxv,nowv)})
