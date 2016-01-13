from django.conf.urls import patterns, url

from api import (
    VersionApi,
    ProjectApi,
    ProjectTypeApi,
    FlowApi,
    EventTypeApi,
    EventApi,
)

urlpatterns = patterns("",

    url(r"^version/$", VersionApi.as_view(), name="version"),
    url(r"^projecttypes/$", ProjectTypeApi.as_view(), name="project-type"),
    url(r"^projects/$", ProjectApi.as_view(), name="project"),
    url(r"^flows/$", FlowApi.as_view(), name="flow"),
    url(r"^eventtypes/$", EventTypeApi.as_view()),
    url(r"^events/$", EventApi.as_view()),

)
