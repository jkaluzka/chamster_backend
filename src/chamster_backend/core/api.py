import datetime

from core.models import ProjectType
from core.serializers import ProjectTypeSerializer
from core.models import Project
from core.serializers import ProjectSerializer
from core.models import Flow
from core.serializers import FlowSerializer
from core.models import EventType
from core.serializers import EventTypeSerializer
from core.models import Event
from core.serializers import EventSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chamster_backend.settings import API_VER

from django.shortcuts import get_object_or_404


class VersionApi(APIView):

    def get(self, request, format=None):
        return Response(API_VER)


class ProjectTypeApi(APIView):

    def get(self, request, format=None):
        types = ProjectType.objects.all()
        serializer = ProjectTypeSerializer(types, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProjectTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectApi(APIView):

    def get(self, request, format=None):
        projects = Project.objects
        query_params = request.query_params
        kwargs = query_params.dict()
        if query_params.get("project_type"):
            kwargs["project_type"] = get_object_or_404(ProjectType, name=query_params.get("project_type"))
        projects = projects.filter(**kwargs).select_related("flow_set")
        # + ordering and pagination
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FlowApi(APIView):

    def get(self, request, format=None):
        flow_list = Flow.objects
        query_params = request.query_params
        if query_params:
            try:
                flow_list = flow_list.filter(project=get_object_or_404(Project,
                    base_project=query_params["base_project"],
                    work_project=query_params["work_project"]))
                # + ordering and pagination
            except KeyError as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = FlowSerializer(flow_list, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        serializer = FlowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventTypeApi(APIView):

    def get(self, request, format=None):
        event_types = EventType.objects.all()
        serializer = EventTypeSerializer(event_types, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EventTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventApi(APIView):

    def get(self, request, format=None):
        query_params = request.query_params
        if query_params:
            kwargs = {}
            # /api/events/?base_project=
            # get all projects for base_project
            # get all flows for above projects
            # use flow_list
            if query_params.get("base_project") and not query_params.get("work_project"):
                print "base_project only"

            # /api/events/?work_project=
            if not query_params.get("base_project") and query_params.get("work_project"):
                print "work_project only"

            # /api/events/?base_project=&work_project=
            # get unique project for base_project + work_project combination
            # find flow list for above project
            # add flow_list to kwargs["flow"] and use it for filtering
            if query_params.get("base_project") and query_params.get("work_project"):
                base_project = query_params.get("base_project")
                work_project = query_params.get("work_project")
                project_id = Project.objects.get(base_project=base_project, work_project=work_project).id
                flow_list = Flow.objects.filter(project=project_id)
                kwargs["flow"] = flow_list

            # /api/events/?base_project=&work_project=&flow=
            # get unique project for base_project + work_project combination
            # find flow list for above project
            # filter above flow list for provided flow number
            # add flow_list to kwargs["flow"] and use it for filtering
            if query_params.get("base_project") and query_params.get("work_project") and query_params.get("flow"):
                base_project = query_params.get("base_project")
                work_project = query_params.get("work_project")
                flow = int(query_params.get("flow"))
                project_id = Project.objects.get(base_project=base_project, work_project=work_project).id
                flow_list = Flow.objects.filter(project=project_id, number=flow)
                kwargs["flow"] = flow_list

            # /api/events/?event_type=
            if query_params.get("event_type"):
                event_type_id = EventType.objects.get(name=query_params.get("event_type")).id
                kwargs["event_type"] = event_type_id

            # /api/events/?flow_number=
            if query_params.get("flow"):
                flow = query_params.get("flow")

            events = Event.objects.filter(**kwargs)

            # + ordering and pagination

        else:
            events = Event.objects.all()

        serializer = EventSerializer(events, many=True)

        for d in serializer.data:
            d["event_type"] = EventType.objects.get(id=d.get("event_type")).name
            flow_id = d["flow"]
            project_id = Flow.objects.get(id=flow_id).project.id
            base_project = Project.objects.get(id=project_id).base_project
            work_project = Project.objects.get(id=project_id).work_project
            d["base_project"] = base_project
            d["work_project"] = work_project
            d["flow"] = Flow.objects.get(id=flow_id).number

        return Response(serializer.data)


    def post(self, request, format=None):
        data = request.data
        flow_number = data.get("flow")

        #TODO: use try-except here
        #find project from Project model according to base_project and work_project
        project = Project.objects.get(base_project=data.get("base_project"), work_project=data.get("work_project"))
        project_id = project.id

        STATUS_SUCCESS = 0

        try:
            flow_id = Flow.objects.get(project=project_id, number=flow_number).id
        except:
            print "warning! could not find flow %s for project %s/%s" % (str(flow_number), data.get("base_project"), data.get("work_project"))
            print "new flow entry will be registered automatically..."
            timestamp = str(datetime.datetime.now())
            comments = "registered automatically by event: %s (timestamp: %s)" % (data.get("event_type"), data.get("timestamp"))
            new_flow = Flow(project=project, number=flow_number, timestamp=timestamp, status=STATUS_SUCCESS, comments=comments)
            new_flow.save()
            print "created new flow entry: {'number': %s, 'project': %s, 'timestamp': '%s', 'comments': '%s'}" % (str(flow_number), str(project_id), timestamp, comments)
            flow_id = new_flow.id

        data["flow"] = flow_id

        data["event_type"] = EventType.objects.get(name=data.get("event_type")).id

        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
