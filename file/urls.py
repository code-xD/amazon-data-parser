from django.urls import path
from .views import home, website_form, retrieveHistoryView, downloadFile, viewCSV

urlpatterns = [
    path('', home, name='home'),
    path('history', retrieveHistoryView, name='retrieve-history'),
    path('<str:website>', website_form, name='website-form'),
    path('download/<str:data_name>', downloadFile, name='download-file'),
    path('view/<str:data_name>', viewCSV, name='view-file')

]
