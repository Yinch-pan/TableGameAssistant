"""
URL configuration for tablegame project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('random', views.randomrole),
    path('add', views.addrole),
    path('role', views.rolenow),
    path('role/detail', views.roledetail),
    path('delete', views.deleaterole),
    path('addset', views.addroleset),
    path('deltmprole', views.deltmprole),
    path('addtmprole', views.addtmprole),
    path('roleset', views.roleset),
    path('delset', views.delset),
    path('editroleset', views.editroleset),
    path('delsetrole', views.delsetrole),
    path('addsetrole', views.addsetrole),
    path('randroleset', views.randroleset),




    path('faceas/cardrecord', views.cardrecord),
    path('faceas/cardrecords', views.cardrecords),
    path('faceas/randomnum', views.randomnum),
    path('faceas/playersit', views.playersit),
    path('faceas/roleskills', views.roleskills),
    path('faceas/roleskills/xushao', views.xushao),
    path('faceas/roleskills/zuxunyou', views.zuxunyou),
    path('faceas', views.faceas),




    path('tables',views.tables),
    path('tables/edittable',views.edittable),
    path('tables/addtable',views.addtable),
    path('tables/update',views.updatetable),
    path('tables/deltable',views.deltable),



    path('skills',views.skills),
    path('skills/refreshskills', views.refreshskills),

    path('', views.homepage),

]
