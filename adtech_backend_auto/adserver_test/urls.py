from django.conf.urls import url
from adserver_test import views

urlpatterns = [
    url(r"^adserver/runTest$", views.results),
    url(r"^adserver/getTestFiles$", views.fileList),
    url(r"^adserver/getTestDirs$", views.dirList),
    url(r"^adserver/cleanCampaign$", views.cleanCampaign),
    url(r"^adserver/getValue$", views.getSpecificValueFromDB)
    ]