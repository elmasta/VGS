from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('ask_email/', views.ask_email, name='ask_email'),
    path('profile/', views.profile_page, name='profile_page'),
    path('logout/', views.user_logout, name='user_logout'),
    path('add_item/', views.add_item, name='add_item'),
    path('add_game/', views.add_game, name='add_game'),
    path('add_DLC/', views.add_DLC, name='add_DLC'),
    path('add_comp/', views.add_comp, name='add_comp'),
    path('add_console/', views.add_console, name='add_console'),
    path('add_addon/', views.add_addon, name='add_addon'),
    path('user_photos/', views.user_photos, name='user_photos'),
    path('user_game_page/<game_id>', views.user_game_page, name='user_game_page'),
    path('user_collection/<plateform_id>', views.user_collection, name='user_collection'),
    path('user_accessory/', views.user_accessory, name='user_accessory'),
    path('user_accessory_page/<accessory_id>', views.user_accessory_page, name='user_accessory_page'),
    path('user_consoles/', views.user_consoles, name='user_consoles'),
    path('user_consoles_page/<consoles_id>', views.user_consoles_page, name='user_consoles_page'),
    path('user_compilations/', views.user_compilations, name='user_compilations'),
    path('user_compilations_page/<compilations_id>', views.user_compilations_page, name='user_compilations_page'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.activate, name='activate'),
    re_path(r'^forgotten_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            views.forgotten_password, name='forgotten_password'),
]
