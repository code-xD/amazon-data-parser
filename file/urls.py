from django.urls import path
from .views import home, website_form

urlpatterns = [
    path('', home, name='home'),
    path('<str:website>', website_form, name='website-form')
]
