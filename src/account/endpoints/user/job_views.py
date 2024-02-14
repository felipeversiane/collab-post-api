from rest_framework.decorators import permission_classes,action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from account.entities.job import Job
from account.serializers.job_serializers import JobSerializer
from rest_framework import viewsets,status
from django.utils.translation import gettext_lazy as _


@permission_classes([IsAuthenticated]) 
class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def list(self,*args, **kwargs):
        queryset = Job.filter(user=self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def read(self, instance,*args, **kwargs):
        if instance.user != self.request.user:
                raise PermissionDenied({"message": _("Permission denied.")})
        serializer = self.get_serializer(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def destroy(self, instance,*args, **kwargs):
        if instance.user != self.request.user:
                raise PermissionDenied({"message": _("Permission denied.")})
        instance.delete()
        return Response({"message":_("Job deleted sucessfully.")},status=status.HTTP_204_NO_CONTENT)
    
    def create(self, serializer,*args, **kwargs):
        serializer.validated_data['user'] = self.request.user
        serializer.save()
        return Response({"message":_("Job created sucessfuly.")},status=status.HTTP_201_CREATED)

    def update(self, serializer,*args, **kwargs):
        item = self.get_object()
        if item.user != self.request.user:
            raise PermissionDenied({"message": _("Permission denied.")})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":_("Job changed sucessfully.")},status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self,serializer,*args, **kwargs):
        item = self.get_object()
        if item.user != self.request.user:
            raise PermissionDenied({"message": _("Permission denied.")})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":_("Job changed sucessfully.")},status=status.HTTP_204_NO_CONTENT)

    