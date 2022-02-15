from django import VERSION
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("talks/", views.talks, name="talks"),
    path("new_talk/<int:type>", views.new_talk, name="new_talk"),
    path("talk/<str:title>", views.talk, name="talk"),
    path("my_talks", views.my_talks, name="my_talks"),

    #API ROUTES
    path("tags", views.tags, name="tags"), 
    path("filter_talks/<int:page>", views.filter_talks, name="filter_talks"),
    path("enroll/<str:title>", views.enroll, name="enroll" ),
    path("get_enrrolled_talks", views.get_enrrolled_talks, name="get_enrrolled_talks")
]
