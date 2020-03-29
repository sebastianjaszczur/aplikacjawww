from django.conf.urls import url

from gallery.views import ImageView, ImageList, AlbumView, AlbumList, ImageCreate

app_name = 'gallery'
urlpatterns = [
    url(r'^$', AlbumList.as_view(), name='album_list'),
    url(r'^images/$', ImageList.as_view(), name='image_list'),
    url(r'^image/(?P<pk>[0-9]+)/(?P<slug>[a-zA-Z0-9\-_]+)$', ImageView.as_view(), name='image_detail'),
    url(r'^upload/$', ImageCreate.as_view(), name='image_upload'),
    url(r'^album/(?P<pk>[0-9]+)/(?P<slug>[a-zA-Z0-9\-_]+)/$', AlbumView.as_view(), name='album_detail'),
    url(r'^album/(?P<apk>[0-9]+)/(?P<pk>[0-9]+)/(?P<slug>[a-zA-Z0-9\-_]+)$', ImageView.as_view(), name='album_image_detail')
]
