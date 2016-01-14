from django.conf.urls import patterns, include, url
from django.contrib import admin

import views

urlpatterns = patterns('',

    # url for UI admin view
    url(r'^admin/', include(admin.site.urls)),

    # url for rest api views
    url(r'^api/', include('core.urls')),

)
