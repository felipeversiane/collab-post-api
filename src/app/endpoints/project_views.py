from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from app.entities.project import Project
from app.serializers.project_serializers import ProjectSerializer
from rest_framework import viewsets,status
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import AllowAny

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.action != 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def list(self,request,*args, **kwargs):
        queryset = self.queryset.exclude(situation__in=['W', 'F'])  
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def read(self, instance,*args, **kwargs):
        serializer = self.get_serializer(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def destroy(self, instance,*args, **kwargs):
        return Response({"message":_("You cannot delete a project.")},status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def create(self, request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({"message":_("Job created successfully.")},status=status.HTTP_201_CREATED)

    def update(self, serializer,*args, **kwargs):
        item = self.get_object()
        if item.user != self.request.user:
            raise PermissionDenied({"message": _("Permission denied.")})
        serializer.is_valid(raise_exception=True)        
        serializer.save()
        return Response({"message":_("Education changed sucessfully.")},status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self,serializer,*args, **kwargs):
        item = self.get_object()
        if item.user != self.request.user:
            raise PermissionDenied({"message": _("Permission denied.")})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":_("Education changed sucessfully.")},status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['GET'])
    def get_projects_by_situation(self, request,*args, **kwargs):
        situation = request.query_params.get('situation')
        situations = ['W', 'O', 'B', 'F']
        if situation not in situations:
            return Response({"message": _("Invalid situation parameter.")}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.queryset.filter(situation=situation,employer=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'])
    def get_budget_mean_by_area(self, request, *args, **kwargs):
        areas = ["FS", "FE", "BE", "GM"]
        area = request.query_params.get('area')
        if area not in areas:
            return Response({"message": _("Invalid area parameter.")}, status=status.HTTP_400_BAD_REQUEST)
        mean_budget = Project.objects.mean_budget(area)
        return Response({"budget_mean": mean_budget}, status=status.HTTP_200_OK)
