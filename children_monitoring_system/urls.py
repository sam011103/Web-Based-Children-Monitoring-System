from django.urls import path
from .views import home_views, auth_views

urlpatterns = [
    path('members/', home_views.members, name='members'),
    path('home/', home_views.home, name='home'),
    path('login/', auth_views.loginIndex, name='login'),
    path('register/', auth_views.registerIndex, name='register'),
    path('logout/', auth_views.logoutIndex)
]