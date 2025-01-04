from django.urls import path,re_path
from . import views
from rest_framework import routers
from django.conf.urls import include


router = routers.DefaultRouter()
router.register(r'user',views.UserViewSet, basename='jobs')
router.register(r'educational',views.EducationalViewSet, basename='educational')
router.register(r'competence',views.CompetenceViewSet, basename='competence')


urlpatterns = [
    re_path('', include(router.urls)),

    re_path(r'^o/(?P<provider>\S+)/$',views.CustomProviderAuthView.as_view(),name='provider-auth'),

    path('jwt/create/', views.CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', views.CustomTokenRefreshView.as_view()),
    path('jwt/verify/', views.CustomTokenVerifyView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    
]