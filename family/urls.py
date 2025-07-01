from django.urls import path
from . import views

urlpatterns = [
    path('', views.person_list, name='person_list'),
    path('add/', views.person_create, name='person_create'),
    path('person/<int:pk>/', views.person_detail, name='person_detail'),
    path('person/<int:pk>/edit/', views.person_update, name='person_update'),
    path('person/<int:pk>/delete/', views.person_delete, name='person_delete'),
    path('relationship-checker/', views.relationship_checker, name='relationship_checker'),
    path('dashboard/', views.dashboard, name='dashboard'),

]



