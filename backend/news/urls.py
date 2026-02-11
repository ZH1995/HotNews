from django.urls import path
from . import views

urlpatterns = [
    path('api/sources/', views.get_sources, name='get_sources'),
    path('api/ranking/<int:source_id>/', views.get_ranking_data, name='get_ranking_data'),
]