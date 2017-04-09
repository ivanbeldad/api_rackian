from rest_framework import routers
from authentication import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='user')
urlpatterns = router.urls
