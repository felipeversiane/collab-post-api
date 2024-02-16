from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from account.entities.job import Job
from account.api.serializers.job_serializers import *
from rest_framework import viewsets,status
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.action != 'get_jobs_by_user':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def list(self,request,*args, **kwargs):
        queryset = self.queryset.filter(user=request.user)  
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def read(self, instance,*args, **kwargs):
        if instance.user != self.request.user:
                raise PermissionDenied({"message": _("Permission denied.")})
        serializer = self.get_serializer(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied({"message": _("Permission denied.")})
        instance.delete()
        return Response({"message": _("Job deleted successfully.")}, status=status.HTTP_204_NO_CONTENT)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({"message":_("Job created successfully.")},status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied({"message": _("Permission denied.")})
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": _("Job changed successfully.")}, status=status.HTTP_200_OK)
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied({"message": _("Permission denied.")})
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": _("Job changed successfully.")}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def get_jobs_by_user(self, request):
        user_uuid = request.query_params.get('user')
        if not user_uuid:
            return Response({"message": _("User UUID is required")}, status=status.HTTP_400_BAD_REQUEST)
        jobs = get_object_or_404(Job, user=user_uuid)
        if jobs.user != request.user:
            raise PermissionDenied({"message": _("You are not authorized to access proposals for this project.")})
        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    