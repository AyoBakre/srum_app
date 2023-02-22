from django.urls import path, include
from . import views

app_name = 'ayomidescrumy'
urlpatterns = [
    path('', views.index, name='about'),
    path('addgoal', views.add_goal, name='addgoal'),
    path('home/', views.home, name='home'),
    path('changegroup/', views.change_goal, name='change_goal'),
    path('movegoal/<int:goal_id>/', views.move_goal, name="movegoal"),
    path('accounts/', include('django.contrib.auth.urls'), name='accounts'),
]
