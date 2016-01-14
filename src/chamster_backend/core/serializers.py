from django.http import QueryDict

from core.models import ProjectType
from core.models import Project
from core.models import Flow
from core.models import EventType
from core.models import Event

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class ProjectTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectType
        fields = ('id', 'name', 'comments')


class ProjectSerializer(serializers.ModelSerializer):

    project_type = serializers.PrimaryKeyRelatedField(many=False, read_only=True, source='project_type.name')
    last_flow_number = serializers.SerializerMethodField('flow_number')
    last_flow_timestamp = serializers.SerializerMethodField('flow_timestamp')
    last_flow_status = serializers.SerializerMethodField('flow_status')
    last_event_type = serializers.SerializerMethodField('event_type')
    last_event_timestamp = serializers.SerializerMethodField('event_timestamp')

    def flow_number(self, project):
        return project.last_flow.number if project.last_flow else 'unknown'

    def flow_timestamp(self, project):
        return project.last_flow.timestamp if project.last_flow else 'unknown'

    def flow_status(self, project):
        return project.last_flow.status if project.last_flow else 'unknown'

    def event_type(self, project):
        try:
            return project.last_flow.last_event.event_type.name
        except AttributeError:
            return 'unknown'

    def event_timestamp(self, project):
        try:
            return project.last_flow.last_event.timestamp
        except AttributeError:
            return 'unknown'

    class Meta:
        model = Project
        fields = (
            'id', 'project_type', 'base_project', 'work_project', 'total_flows', 'last_flow_number',
            'last_flow_timestamp', 'last_flow_status', 'total_events', 'last_event_type',
            'last_event_timestamp', 'project_url', 'comments',
        )

    def is_valid(self, raise_exception=False):
        is_validated = super(ProjectSerializer, self).is_valid(raise_exception)
        if is_validated:
            try:
                # if request is django HttpRequest type, then cast to regular python dict
                data = self.initial_data.dict() if isinstance(self.initial_data, QueryDict) else self.initial_data
                project_type = ProjectType.objects.get(name=data.get('project_type'))
                self.validated_data['project_type'] = project_type
            except ProjectType.DoesNotExist:
                raise ValidationError('validation error')
        return is_validated


class FlowSerializer(serializers.ModelSerializer):
    base_project = serializers.PrimaryKeyRelatedField(many=False, read_only=True, source='project.base_project')
    work_project = serializers.PrimaryKeyRelatedField(many=False, read_only=True, source='project.work_project')
    last_event_type = serializers.SerializerMethodField('event_type')
    last_event_timestamp = serializers.SerializerMethodField('event_timestamp')

    def event_type(self, flow):
        try:
            return flow.last_event.event_type.name
        except AttributeError:
            return 'unknown'

    def event_timestamp(self, flow):
        try:
            return flow.last_event.timestamp
        except AttributeError:
            return 'unknown'

    class Meta:
        model = Flow
        fields = (
            'id', 'number', 'timestamp', 'status', 'comments', 'base_project',
            'work_project', 'total_events', 'last_event_type', 'last_event_timestamp'
        )

    def is_valid(self, raise_exception=False):
        is_validated = super(FlowSerializer, self).is_valid(raise_exception)
        if is_validated:
            try:
                # if request is django HttpRequest type, then cast to regular python dict
                data = self.initial_data.dict() if isinstance(self.initial_data, QueryDict) else self.initial_data
                project = Project.objects.get(
                    base_project=data.get('base_project'),
                    work_project=data.get('work_project')
                )
                self.validated_data['project'] = project
            except Project.DoesNotExist:
                raise ValidationError('validation error')
        return is_validated


class EventTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventType
        fields = ('id', 'name', 'comments')


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = (
            'id', 'flow', 'event_type', 'timestamp', 'user', 'comments'
        )
