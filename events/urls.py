from django.urls import path

from .views import seasons

urlpatterns = [
    path("seasons/frc/", seasons.get_frc_seasons),
]