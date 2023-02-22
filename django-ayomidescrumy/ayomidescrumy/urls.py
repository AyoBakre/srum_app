from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'ayomidescrumy'
urlpatterns = [
    path('', views.index, name='index'),
    path('addgoal', views.add_goal, name='addgoal'),
    path('home', views.home, name='home'),
    path('movegoal/<int:goal_id>/', views.move_goal, name="movegoal"),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
]
