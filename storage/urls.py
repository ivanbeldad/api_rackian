from rest_framework import routers
from storage import views

router = routers.DefaultRouter()
router.register(r'folders', views.FolderViewSet, base_name='folder')
urlpatterns = router.urls
