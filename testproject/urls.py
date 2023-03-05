from django.urls import include, re_path

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    re_path(r'^', include('simplesshkey.urls', namespace='simplesshkey')),
    re_path(r'^admin/', admin.site.urls),
]
