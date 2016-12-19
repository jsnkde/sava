from django.conf.urls import url

from . import views

app_name = 'catalog'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^item/(?P<pk>[0-9]+)$', views.ItemView.as_view(), name='detail'),
    url(r'^item/(?P<pk>[0-9]+)/edit$', views.ItemUpdateView.as_view(), name='edit_item'),
    url(r'^item/(?P<pk>[0-9]+)/delete$', views.ItemUpdateView.as_view(done=True), name='delete_item'),
    url(r'^item/new$', views.ItemCreateView.as_view(), name='new_item'),
    url(r'^my/', views.IndexView.as_view(my=True), name='profile'),
]
