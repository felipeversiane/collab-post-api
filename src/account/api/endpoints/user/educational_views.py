from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from account.entities.education_background import EducationalBackground as Educational
from account.api.serializers.educational_serializers import *
from rest_framework import viewsets,status
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404


class EducationalViewSet(viewsets.ModelViewSet):
    queryset = Educational.objects.all()
    serializer_class = EducationalSerializer

    def get_permissions(self):
        if self.action != 'get_educationals_by_user':
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

    def destroy(self, instance,*args, **kwargs):
        if instance.user != self.request.user:
                raise PermissionDenied({"message": _("Permission denied.")})
        instance.delete()
        return Response({"message":_("Education deleted sucessfully.")},status=status.HTTP_204_NO_CONTENT)
    
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
    def get_educational_by_user(self, request):
        user_uuid = request.query_params.get('user')
        if not user_uuid:
            return Response({"message": _("User UUID is required")}, status=status.HTTP_400_BAD_REQUEST)
        educationals = get_object_or_404(Educational, user=user_uuid)
        if educationals.user != request.user:
            raise PermissionDenied({"message": _("You are not authorized to access proposals for this project.")})
        serializer = self.get_serializer(educationals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    