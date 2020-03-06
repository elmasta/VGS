from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('profile/', views.profile_page, name='profile_page'),
    path('logout/', views.user_logout, name='user_logout'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate'),
]
