from django.conf.urls import url
from rest_framework import routers
from . import views


router = routers.SimpleRouter()
router.register(r'permissions', views.PermissionViewset, base_name='permission')
router.register(r'filelinks', views.FileLinkViewset, base_name='filelink')
router.register(r'folderlinks', views.FolderLinkViewset, base_name='folderlink')

urlpatterns = router.urls


urlpatterns += [
    url(r'^share/file/(?P<id>[a-zA-Z0-9\-_]*)/', views.ShareFileView.as_view(), name='share-file'),
    url(r'^share/folder/(?P<id>[a-zA-Z0-9\-_]*)/', views.ShareFolderView.as_view(), name='share-folder'),
    # url(r'^share-folders/', views.FolderLinkViewset.as_view({'get': 'list'}), name='share-folder'),
]
