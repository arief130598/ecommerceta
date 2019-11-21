from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('get-task-info', views.get_task_info, name='gettask'),
]