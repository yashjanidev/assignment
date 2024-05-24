from django.urls import path
from .views import *

urlpatterns = [
    path('clients/', ClientList.as_view(), name='client-list'),
    path('client-create/', ClientCreate.as_view(), name='client-create'),
    path('clients/<int:pk>/', ClientReadUpdateDeleteDetail.as_view(),
         name='client-read-update-delete'),
    path('client/<int:pk>/', ClientDelete.as_view(),
         name='client-destroy'),
    path('clients/<int:pk>/projects/',
         ProjectCreate.as_view(), name='project-create'),
    path('projects/', ProjectList.as_view(), name='project-list'),
]
