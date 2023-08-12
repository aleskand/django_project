from django.urls import path
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("snp/", views.index, name="index"),
    path('export-csv/', views.export_csv, name='export-csv'),
    path("species/<int:id>", views.species_details, name="species_details"),
    path("annotation/<int:id>", views.annotation_details, name="annotation_details")
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)