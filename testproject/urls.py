from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
  url(r'^', include('django_sshkey.urls', namespace='django_sshkey')),
  url(r'^admin/', include(admin.site.urls)),
]
