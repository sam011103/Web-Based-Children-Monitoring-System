from django.urls import path
from .views import home_views, auth_views
from .views.auth_views import UserRegisterView

urlpatterns = [
    path('members/', home_views.members, name='members'),
    path('home/', home_views.home, name='home'),
    path('login/', auth_views.loginIndex, name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('logout/', auth_views.logoutIndex)
]