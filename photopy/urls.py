from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'PhotoBook.views.ingresar', name='home'),
    # url(r'^photopy/', include('photopy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^usuario/nuevo$', 'PhotoBook.views.nuevo_usuario'),
    url(r'^ingresar/$', 'PhotoBook.views.ingresar'),
    url(r'^privado/$', 'PhotoBook.views.privado'),
    url(r'^cerrar/$', 'PhotoBook.views.cerrar'),
    url(r'^album/([a-z0-9]{1,20})/$', 'PhotoBook.views.listaAlbum'),
    url(r'^foto/([a-zA-Z0-9]{1,20})/$', 'PhotoBook.views.listaFoto'),
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
