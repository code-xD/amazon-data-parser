from django.urls import path
from .views import home, downloadFile, viewCSV

urlpatterns = [
    path('', home, name='home'),
    path('download/<str:data_name>', downloadFile, name='download-file'),
    path('view/<str:data_name>', viewCSV, name='view-file')

]
