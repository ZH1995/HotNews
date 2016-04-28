from django.conf.urls import *
from blog.views import index
 
urlpatterns = patterns('',
                      url(r'^$',index),
                      )