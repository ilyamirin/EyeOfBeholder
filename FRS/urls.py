from . import views

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.redirect_view, name='index'),
    url(r'^stream/$', views.stream, name='stream'),
    url(r'^faces/$', views.faces, name='faces'),
    url(r'^\S+save_name/$', views.save_name, name='save_name'),
    url(r'^\S+delete_name/$', views.delete_name, name='delete_name'),
    url(r'^\S+merge_names/$', views.merge_names, name='merge_name'),
    url(r'^faces/filtered_faces/$', views.filtered_faces, name='filtered_faces'),
    url(r'^faces/journal/$', views.journal, name='journal'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


