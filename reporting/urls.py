from reporting import views
from django.urls import path

urlpatterns = [
    path('report/', views.report, name='report'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accept-task/<slug:rID>', views.acceptTask, name='acceptTask'),
    path('solve-task/<slug:rID>', views.solveTask, name='solveTask')
]