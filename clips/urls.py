from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('top/week/', views.topweek, name='topweek'),
    path('top/month/', views.topmonth, name='topmonth'),
    path('top/alltime/', views.topalltime, name='topalltime'),
    path('search/', views.search, name='search_results'),
    path('stats/', views.statistics, name='statistics')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
