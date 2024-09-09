from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('likepost', views.likepost, name='likepost'),
    path('follow', views.follow, name='follow'),
    path('setting', views.setting, name='setting'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('logout', views.logout, name='logout'),
]
