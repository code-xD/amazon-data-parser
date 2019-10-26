from django.urls import path
from .views import home, website_form, retrieveHistoryView, downloadFile

urlpatterns = [
    path('', home, name='home'),
    path('history', retrieveHistoryView, name='retrieve-history'),
    path('<str:website>', website_form, name='website-form'),
    path('download/<str:data_name>', downloadFile, name='download-file')
]
