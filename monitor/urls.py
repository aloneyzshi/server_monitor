from django.conf.urls import include, url
from  monitor import views


urlpatterns = [
    url(r'^system/$', views.index, name='monitor'),
    url(r'^api/clientconf/(?P<id>\d+)/$',views.send_config,name='send_config'),
    #url(r'api/update/$',views.receive_data,name='receive_data'),
    url(r'api/update/$',views.test_receive,name='receive_data'),
    url(r'hostinfo/(?P<id>\d+)/$',views.get_data,name='hostinfo')
]