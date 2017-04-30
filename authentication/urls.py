from django.conf.urls import url
from rest_framework import routers
from authentication import views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet, base_name='user')
# urlpatterns = router.urls

urlpatterns = [
    url(r'^token/$', views.TokenView.as_view(), name='token'),
    url(r'^user/$', views.UserViewSet.as_view(), name='user'),
]
