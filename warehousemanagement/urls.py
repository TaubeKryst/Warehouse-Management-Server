from .views import ProductListView, ProductRudView
from django.conf.urls import url

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='post-create'),
    url(r'^(?P<pk>\d+)/$', ProductRudView.as_view(), name='post-rud'),
]
