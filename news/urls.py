from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/ranking/<int:source_id>/', views.get_ranking_data, name='get_ranking_data'),
]