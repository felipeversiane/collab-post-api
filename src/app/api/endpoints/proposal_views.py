from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from app.entities.proposal import Proposal
from app.api.serializers.proposal_serializers import *
from rest_framework import viewsets,status
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from app.entities.project import Project
from django.shortcuts import get_object_or_404


class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]

    def list(self,request,*args, **kwargs):
        queryset = self.queryset.filter(freelancer = request.user) 
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def read(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.freelancer != request.user and instance.project.employer != request.user:
            raise PermissionDenied({"message": _("Permission denied.")})
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, instance,*args, **kwargs):
        if instance.freelancer != self.request.user:
                raise PermissionDenied({"message": _("Permission denied.")})
        instance.delete()
        return Response({"message":_("Education deleted sucessfully.")},status=status.HTTP_204_NO_CONTENT)
    
    def create(self, request, *args, **kwargs):
        project_id = request.data.get('project')
        existing_proposals = Proposal.objects.filter(project=project_id, freelancer=request.user)
        if existing_proposals.exists():
            raise ValidationError(_({"message":"You have already submitted a proposal for this project."},code='invalid'))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(freelancer=request.user)
        return Response({"message":_("Proposal created successfully.")}, status=status.HTTP_201_CREATED)

    def update(self, serializer,*args, **kwargs):
        item = self.get_object()
        if item.situation != 'W':
            raise PermissionDenied({"message":_("It is not possible to edit it.")})
        if item.freelancer != self.request.user:
            raise PermissionDenied({"message": _("Permission denied.")})
        serializer.is_valid(raise_exception=True)        
        serializer.save()
        return Response({"message":_("Education changed sucessfully.")},status=status.HTTP_204_NO_CONTENT)
    
    def partial_update(self,serializer,*args, **kwargs):
        item = self.get_object()
        if item.situation != 'W':
            raise PermissionDenied({"message":_("It is not possible to edit it.")})
        if item.user != self.request.user:
            raise PermissionDenied({"message": _("Permission denied.")})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":_("Education changed sucessfully.")},status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['GET'])
    def get_proposals_by_project(self,request,*args, **kwargs):
        project_uuid = request.query_params.get('project')
        if not project_uuid:
            return Response({"message": _("Project UUID is required.")}, status=status.HTTP_400_BAD_REQUEST)
        
        project = get_object_or_404(Project, uuid=project_uuid)
        if project.employer != request.user:
            raise PermissionDenied({"message": _("You are not authorized to access proposals for this project.")})
        
        proposals = self.queryset.filter(project=project_uuid)
        serializer = self.get_serializer(proposals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    