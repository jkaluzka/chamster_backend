import json
from urllib import urlencode
from django.core.urlresolvers import reverse
from django.test import TestCase
from model_mommy import mommy

from chamster_backend.settings import API_VER

from core.models import (
    Project,
    ProjectType,
    Flow,
    Event,
    EventType,
)

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class VersionApiTestCases(TestCase):
    """
    Test class for rest api VersionApi class
    """

    def _get(self, url=None):
        url = url or reverse("version")
        return self.client.get(url)

    def test_getting_api_version(self):
        resp = self._get()
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = json.loads(resp.content)
        self.assertEqual(data, API_VER)


class ProjectTypeApiTestCases(TestCase):
    """
    Test class for rest api ProjectTypeApi class
    """

    def setUp(self):
        self.project_type1 = mommy.make(ProjectType, name="priv")
        self.project_type2 = mommy.make(ProjectType, name="prod")
        self.project_type3 = mommy.make(ProjectType, name="scm")

    def tearDown(self):
        ProjectType.objects.all().delete()

    def _get(self, url=None):
        url = url or reverse("project-type")
        return self.client.get(url)

    def test_getting_all_project_types(self):
        response = self._get()
        self.assertEqual(response.status_code, HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

    def test_post_request(self):
        resp = self.client.post("/api/projecttypes/", {"name": "type-x", "comments": "project type: type-x"})
        self.assertEqual(resp.status_code, HTTP_201_CREATED)

    def test_duplicated_post_request(self):
        resp = self.client.post("/api/projecttypes/", {"name": "type-x", "comments": "project type: type-x"})
        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        resp = self.client.post("/api/projecttypes/", {"name": "type-x", "comments": "project type: type-x"})
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)


class ProjectApiTestCases(TestCase):
    """
    Test class for rest api ProjectApi class
    """

    def setUp(self):
        self.first_flow_timestamp = "2015-12-28T20:12:16Z"
        self.last_flow_number = 2
        self.last_flow_timestamp = "2015-12-28T22:12:16Z"
        self.last_flow_status = 1

        self.first_event_timestamp = "2015-12-28T21:12:16Z"
        self.last_event_type = "EVENT TYPE 1"
        self.last_event_timestamp = "2015-12-28T23:12:16Z"

        self.project_type1 = mommy.make(ProjectType, name="priv")
        self.project_type2 = mommy.make(ProjectType, name="prod")
        self.project_type3 = mommy.make(ProjectType, name="scm")

        self.project1 = mommy.make(Project, project_type=self.project_type1, base_project="base_project", work_project="work_project")
        self.project2 = mommy.make(Project, project_type=self.project_type2, base_project="base_project2", work_project="work_project2")
        self.project3 = mommy.make(Project, project_type=self.project_type3, base_project="base_project3", work_project="work_project3")
        self.project4 = mommy.make(Project, project_type=self.project_type1, base_project="base_project4", work_project="work_project4")

        self.flow1 = mommy.make(Flow, project=self.project1, timestamp=self.first_flow_timestamp)
        self.flow2 = mommy.make(Flow, project=self.project1, number=self.last_flow_number, timestamp=self.last_flow_timestamp, status=self.last_flow_status)
        self.flow3 = mommy.make(Flow, project=self.project2)
        self.flow4 = mommy.make(Flow, project=self.project3)
        self.flow5 = mommy.make(Flow, project=self.project4)

        self.event_type1 = mommy.make(EventType, name=self.last_event_type)

        self.event1 = mommy.make(Event, flow=self.flow1, timestamp=self.first_event_timestamp)
        self.event2 = mommy.make(Event, flow=self.flow2, event_type=self.event_type1, timestamp=self.last_event_timestamp)

        self.event3 = mommy.make(Event, flow=self.flow3)
        self.event4 = mommy.make(Event, flow=self.flow4)
        self.event5 = mommy.make(Event, flow=self.flow5)

    def tearDown(self):
        ProjectType.objects.all().delete()
        Project.objects.all().delete()

    def _get(self, url=None, params=None):
        url = url or reverse("project")
        if params:
            url = "{url}?{params}".format(url=url, params=urlencode(params))
        return self.client.get(url)

    def test_get_returns_response_HTTP_200_OK(self):
        response = self._get()
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_getting_all_projects(self):
        response = self._get()
        data = json.loads(response.content)
        self.assertEqual(len(data), 4)

    def test_getting_only_priv_projects(self):
        params = {"project_type": self.project_type1.name}
        response = self._get(params=params)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def test_getting_projects_with_proper_protocol(self):
        self.maxDiff = None
        params = {"project_type": self.project_type1.name}
        response = self._get(params=params)
        data = json.loads(response.content)
        expected = [
            {
                "id": self.project1.id,
                "total_flows": 2,
                "last_flow_number": self.last_flow_number,
                "last_flow_timestamp": self.last_flow_timestamp,
                "last_flow_status": self.last_flow_status,
                "total_events": 2,
                "last_event_type": self.last_event_type,
                "last_event_timestamp": self.last_event_timestamp,
                "project_type": self.project_type1.name,
                "base_project": self.project1.base_project,
                "work_project": self.project1.work_project,
                "project_url": self.project1.project_url,
                "comments": self.project1.comments,
            },
            {
                "id": self.project4.id,
                "total_flows": 0,
                "last_flow_number": "unknown",
                "last_flow_timestamp": "unknown",
                "last_flow_status": "unknown",
                "total_events": 0,
                "last_event_type": "unknown",
                "last_event_timestamp": "unknown",
                "project_type": self.project_type1.name,
                "base_project": self.project4.base_project,
                "work_project": self.project4.work_project,
                "project_url": self.project4.project_url,
                "comments": self.project4.comments,
            },
        ]
        self.assertEqual(len(data), 2)
        self.assertDictEqual(data[0], expected[0])

    def test_getting_projects_by_base_project(self):
        params = {"base_project": self.project1.base_project}
        response = self._get(params=params)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], self.project1.id)

    def test_getting_projects_by_work_project(self):
        params = {"work_project": self.project4.work_project}
        response = self._get(params=params)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], self.project4.id)

    def test_getting_projects_by_wrong_base_project(self):
        params = {"base_project": "wrong_base_project"}
        response = self._get(params=params)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

    def test_getting_projects_by_wrong_work_project(self):
        params = {"work_project": "wrong_work_project"}
        response = self._get(params=params)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

    def test_post_request(self):
        project_type_5 = ProjectType(name="project_type_5", comments="some comments")
        project_type_5.save()
        resp = self.client.post(
            "/api/projects/",
            {
                "project_type": project_type_5.name,
                "base_project": "base_project_5",
                "work_project": "work_project_5",
                "project_url": "some url here",
                "comments": "comments related to project: base_project_5/work_project_5",
            })
        self.assertEqual(resp.status_code, HTTP_201_CREATED)


class FlowApiTestCases(TestCase):
    """
    Test class for rest api FlowApi class
    """

    def setUp(self):
        self.project1 = mommy.make(Project, base_project="base_project", work_project="work_project")
        self.project2 = mommy.make(Project, base_project="base_project2", work_project="work_project2")
        self.project3 = mommy.make(Project, base_project="base_project3", work_project="work_project3")
        self.project4 = mommy.make(Project, base_project="base_project4", work_project="work_project4")

        self.flow1_project1 = mommy.make(Flow, project=self.project1, number=1)
        self.flow2_project1 = mommy.make(Flow, project=self.project1, number=2)
        self.flow3_project1 = mommy.make(Flow, project=self.project1, number=3)
        self.flow1_project2 = mommy.make(Flow, project=self.project2, number=1)
        self.flow2_project2 = mommy.make(Flow, project=self.project2, number=2)
        self.flow1_project3 = mommy.make(Flow, project=self.project3, number=1)
        self.flow2_project3 = mommy.make(Flow, project=self.project3, number=2)

    def tearDown(self):
        Flow.objects.all().delete()
        Project.objects.all().delete()

    def _get(self, url=None, params=None):
        url = url or reverse("flow")
        if params:
            url = "{url}?{params}".format(url=url, params=urlencode(params))
        return self.client.get(url)

    def test_getting_all_flows(self):
        response = self._get()
        self.assertEqual(response.status_code, HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 7)

    def test_getting_flows_in_correct_order(self):
        response = self._get()
        data = json.loads(response.content)
        self.assertEqual(data[0]["number"], self.flow1_project1.number)
        self.assertEqual(data[2]["number"], self.flow3_project1.number)
        # TODO: check for more projects

    def test_getting_flows_with_proper_protocol(self):
        response = self._get()
        data = json.loads(response.content)
        expected = {
            "id": self.flow1_project1.id,
            "total_events": 0,
            "last_event_type": "unknown",
            "last_event_timestamp": "unknown",
            "base_project": self.project1.base_project,
            "work_project": self.project1.work_project,
            "number": self.flow1_project1.number,
            "timestamp": self.flow1_project1.timestamp.strftime(DATETIME_FORMAT),
            "status": self.flow1_project1.status,
            "comments": self.flow1_project1.comments,
        }
        self.assertDictEqual(data[0], expected)

    def test_flow_doesnt_contain_project_field(self):
        response = self._get()
        data = json.loads(response.content)
        self.assertIsNone(data[0].get("project"))

    def test_retrieving_400_bad_request(self):
        params = {"base_project": "fake_base_project"}
        response = self._get(params=params)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

        params = {"work_project": "fake_work_project"}
        response = self._get(params=params)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_getting_flows_with_correct_params(self):
        params = {
            "base_project": self.project2.base_project,
            "work_project": self.project2.work_project,
        }
        response = self._get(params=params)
        self.assertEqual(response.status_code, HTTP_200_OK)
        data = json.loads(response.content)
        expected = [
            {
                "id": self.flow1_project2.id,
                "total_events": 0,
                "last_event_type": "unknown",
                "last_event_timestamp": "unknown",
                "base_project": self.project2.base_project,
                "work_project": self.project2.work_project,
                "number": self.flow1_project2.number,
                "timestamp": self.flow1_project2.timestamp.strftime(DATETIME_FORMAT),
                "status": self.flow1_project2.status,
                "comments": self.flow1_project2.comments,
            },
            {
                "id": self.flow2_project2.id,
                "total_events": 0,
                "last_event_type": "unknown",
                "last_event_timestamp": "unknown",
                "base_project": self.project2.base_project,
                "work_project": self.project2.work_project,
                "number": self.flow2_project2.number,
                "timestamp": self.flow2_project2.timestamp.strftime(DATETIME_FORMAT),
                "status": self.flow2_project2.status,
                "comments": self.flow2_project2.comments,
            },
        ]
        self.assertListEqual(data, expected)

    def test_flow_not_found_with_wrong_params(self):
        params = {
            "base_project": self.project2.base_project,
            "work_project": "wrong_work_project",
        }
        response = self._get(params=params)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_flow_not_found_with_params_mixed_from_projects(self):
        params = {
            "base_project": self.project2.base_project,
            "work_project": self.project3.work_project,
        }
        response = self._get(params=params)
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_empty_flow_list(self):
        params = {
            "base_project": self.project4.base_project,
            "work_project": self.project4.work_project,
        }
        response = self._get(params=params)
        self.assertEqual(response.status_code, HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

    def test_post_request(self):
        project_type = ProjectType(name="project_type_1", comments="some comments")
        project_type.save()
        project = Project(
            project_type=project_type,
            base_project="base_project_5",
            work_project="work_project_5",
            project_url="some url",
            comments="comments related to this project",
        )
        project.save()
        resp = self.client.post(
            "/api/flows/",
            {
                "number": 5,
                "base_project": project.base_project,
                "work_project": project.work_project,
                "timestamp": "2015-12-23T12:34:56.000Z",
                "status": 0,
                "comments": "comments related to project",
            })
        self.assertEqual(resp.status_code, HTTP_201_CREATED)
        self.assertEqual(len(Flow.objects.filter(project=project)), 1)

    def test_post_raise_400_when_empty_data(self):
        resp = self.client.post("/api/flows/", {})
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)

    def test_post_raise_400_when_missing_number(self):
        project_type = ProjectType(name="project_type_1", comments="some comments")
        project_type.save()
        project = Project(
            project_type=project_type,
            base_project="base_project_5",
            work_project="work_project_5",
            project_url="some url",
            comments="comments related to this project",
        )
        project.save()
        resp = self.client.post(
            "/api/flows/",
            {
                "base_project": project.base_project,
                "work_project": project.work_project,
                "timestamp": "2015-12-23T12:34:56.000Z",
                "status": 0,
                "comments": "comments related to project",
            })
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)

    def test_post_raise_400_when_missing_base_project(self):
        project_type2 = ProjectType(name="project_type_2", comments="some comments")
        project_type2.save()
        project2 = Project(
            project_type=project_type2,
            base_project="base_project_5",
            work_project="work_project_5",
            project_url="some url",
            comments="comments related to this project",
        )
        project2.save()
        resp = self.client.post(
            "/api/flows/",
            {
                "number": 7,
                "work_project": project.work_project,
                "timestamp": "2015-12-23T12:34:56.000Z",
                "status": 0,
                "comments": "comments related to project",
            })
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)

    def test_post_raise_400_when_project_not_found(self):
        resp = self.client.post(
            "/api/flows/",
            {
                "number": 7,
                "base_project": "wrong_base_project",
                "work_project": "wrong_work_project",
                "timestamp": "2015-12-23T12:34:56.000Z",
                "status": 0,
                "comments": "comments related to project",
            })
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)


class EventTypeApiTestCases(TestCase):
    """
    Test class for rest api EventTypeApi class
    """

    def test_post_request(self):
        resp = self.client.post(
            "/api/eventtypes/",
            {"name": "EVENT_XYZ", "comments": "comments related to EVENT_XYZ"}
        )
        self.assertEqual(resp.status_code, HTTP_201_CREATED)


class EventApiTestCases(TestCase):
    """
    Test class for rest api EventApi class
    """

    def test_post_request(self):
        project_type = ProjectType(name="project_type_1", comments="some comments")
        project_type.save()
        project = Project(
            project_type=project_type,
            base_project="base_project",
            work_project="work_project",
            project_url="some url",
            comments="comments related to this project",
        )
        project.save()
        event_type = EventType(name="EVENT_XYZ", comments="comments related to EVENT_XYZ")
        event_type.save()
        resp = self.client.post(
            "/api/events/",
            {
                "flow": 12,
                "event_type": event_type.name,
                "base_project": project.base_project,
                "work_project": project.work_project,
                "timestamp": "2015-11-12T15:16:17.000Z",
                "user": "someuser",
                "comments": "some comments related to event"
            },
        )
        self.assertEqual(resp.status_code, HTTP_201_CREATED)
