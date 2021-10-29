from django.urls import path, re_path
from .views import *

app_name = 'pkmnapi'

urlpatterns = [
    path('', main),
    path('load/', load),
    path('show/', show),
    re_path(r'^pokemon.*$', pokemon),
]
