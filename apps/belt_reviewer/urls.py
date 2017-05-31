from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^books/add$', views.add_books),
    url(r'^add$', views.add),
    url(r'^books/(?P<id>\d+)$', views.book),
    url(r'^books/$', views.books),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^users/(?P<id>\d+)$', views.users),

]
