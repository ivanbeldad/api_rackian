from django.conf.urls import url
from authentication import views

urlpatterns = [
    url(r'^token/$', views.TokenView.as_view(), name='token'),
    url(r'^user/(?P<pk>[a-zA-Z0-9]{12})/$', views.UserViewSet.as_view(), name='user-detail'),
]
