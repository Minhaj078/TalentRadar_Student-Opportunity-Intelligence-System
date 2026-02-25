from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('auto-application/', views.auto_application, name='auto_application'),
    path('community/', views.community, name='community'),
    path('apply/<int:opp_id>/', views.apply_opportunity, name='apply_opportunity'),
]