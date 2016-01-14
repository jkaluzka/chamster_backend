from django import forms
from django.contrib import admin
from django.forms import TextInput

from core.models import ProjectType
from core.models import Project
from core.models import Flow
from core.models import EventType
from core.models import Event


class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'comments')
    list_display_links = list_display
admin.site.register(ProjectType, ProjectTypeAdmin)


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('project_type', 'base_project', 'work_project', 'project_url', 'comments')
        widgets = {
            'base_project': TextInput(attrs={'size': 64}),
            'work_project': TextInput(attrs={'size': 64}),
            'project_url': TextInput(attrs={'size': 128}),
        }


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    list_display = ('id', 'project_type', 'base_project', 'work_project', 'project_url', 'comments')
    list_display_links = list_display
    list_filter = ('project_type', 'base_project', 'work_project')
admin.site.register(Project, ProjectAdmin)


class FlowForm(forms.ModelForm):

    class Meta:
        model = Flow
        fields = ('project', 'number', 'timestamp', 'status', 'comments')
        widgets = {
            'comments': TextInput(attrs={'size': 64}),
        }


class FlowAdmin(admin.ModelAdmin):
    form = FlowForm
    list_display = ('id', 'project', 'number', 'timestamp', 'status', 'comments')
    list_display_links = list_display
    list_filter = ('project', 'timestamp')
admin.site.register(Flow, FlowAdmin)


class EventTypeForm(forms.ModelForm):

    class Meta:
        model = EventType
        fields = ('name', 'comments')
        widgets = {
            'name': TextInput(attrs={'size': 64}),
        }


class EventTypeAdmin(admin.ModelAdmin):
    form = EventTypeForm
    list_display = ('id', 'name', 'comments')
    list_display_links = list_display
admin.site.register(EventType, EventTypeAdmin)


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('flow', 'event_type', 'user', 'timestamp', 'comments')
        widgets = {
            'comments': TextInput(attrs={'size': 64}),
        }


class EventAdmin(admin.ModelAdmin):
    form = EventForm
    list_display = ('id', 'flow', 'event_type', 'user', 'timestamp', 'comments')
    list_display_links = list_display
    list_filter = ('user', 'timestamp')
    list_per_page = 20
admin.site.register(Event, EventAdmin)
