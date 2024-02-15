from django.urls import path,re_path
from . import views
from django.conf.urls import include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'project',views.ProjectViewSet,basename='project')
router.register(r'proposal',views.ProposalViewSet,basename='proposal')

urlpatterns = [
    re_path('', include(router.urls)),
    
]