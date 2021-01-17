from django.urls import path
from django.conf.urls import include, url
from .views import profileView,ProfilesDetail,Updateprofile
app_name = 'profile'
urlpatterns = [
    path('profile/<username>', profileView.as_view(), name='profiles'),
    path('profile/<str:slug>',ProfilesDetail.as_view(),name="Profiles_detail"),
    path('profile/<str:slug>/update/',Updateprofile.as_view(),name="update_profile"),

]