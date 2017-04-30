from django.conf.urls import url
from rest_framework import routers
from storage import views

router = routers.DefaultRouter()
router.register(r'folders', views.FolderViewSet, base_name='folder')
router.register(r'files', views.FileViewSet, base_name='file')
urlpatterns = router.urls

urlpatterns += [
    url(r'^download/(?P<id>[a-zA-Z0-9\-_]*)/',
        views.DownloadableFileView.as_view(), name='download'),
]
