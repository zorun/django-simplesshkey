# updating to django 4.x
# from django.conf.urls import include, url
from django.urls import include, re_path as url


from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^', include('simplesshkey.urls', namespace='simplesshkey')),
    url(r'^admin/', admin.site.urls),
]
