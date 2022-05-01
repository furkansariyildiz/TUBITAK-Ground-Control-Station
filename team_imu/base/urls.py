from django.contrib import admin
from django.urls import path
from base import views

urlpatterns = [
    path("register/",views.register,name="register"), 
    path("login/",views.loginUser,name="login"),
    path("logout/",views.logoutUser,name="logout"),
    path('result/',views.result,name="result"),
    path('board/',views.board,name="board"),
    path('result/detail/<int:id>',views.detail,name="detail"),
    path('result/update/<int:id>',views.update,name="update"),
    path('result/delete/<int:id>',views.delete,name="delete"),
    path('photos/',views.photos,name="photos"),
    path('photos_use/<int:id>',views.photos_use,name="photos_use"),
    path('add_photo/<path:slug>',views.add_photo,name="add_photo"),
    path('delete_photo/<path:slug>',views.delete_photo,name="delete_photo"),
    path('map/',views.maps,name="maps"),
    path('map/image_paths', views.ImagesPaths, name="image_paths"),
    path('map/googlemaps', views.googlemaps.map, name = "googlemaps"),
    path('map/control', views.Control, name="control"),
    #path('chatbot', views.Chatbot),
    #burada url = "/base/"den sonrası için açılmış urls kısmı
    #örneğin /base/board/ için buraya uğrayacak ve views.board'a bakacak.
]
