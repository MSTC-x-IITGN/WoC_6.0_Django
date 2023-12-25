from management import views
from django.urls import path

urlpatterns = [
    path('login/', views.userlogin, name='userlogin'),
    path('logout/', views.userlogout, name='userlogout'),     
    path('register/', views.register, name='register'),
    path('register/volunteer', views.volregister, name='volregister'),
    path('register/organization', views.orgregister, name='orgregister'),
    path('resources/', views.resources, name='resources'),
    path('add-resource/', views.addResource, name='addResource'),
    path('edit-resource/<slug:rID>', views.editResource, name='editResource'),
    path('delete-resource/<slug:rID>', views.delResource, name='delResource'),
    path('volunteers/', views.volunteers, name='volunteers')
]