"""IMDBSearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('message_queue_send', views.message_queue_send, name='message_queue_send'),
    path('message_queue_rcv', views.message_queue_rcv, name='message_queue_rcv'),
    #GET
    path('get_names', views.get_names, name='get_names'),
    path('get_principal', views.get_principal, name='get_principal'),
    path('get_ratings', views.get_ratings, name='get_ratings'),
    path('get_basic', views.get_basic, name='get_basic'),
    path('get_titletoname', views.get_titletoname, name='get_titletoname'),
    path('consumer_start', views.consumers_start, name='consumer_start'),
    #POST
    path('add_basic', views.add_basic, name='add_basic'),
    path('add_name', views.add_name, name='add_name'),
    path('add_principal', views.add_principal, name='add_principal'),
    path('add_titletoname', views.add_titletoname, name='add_titletoname'),
    path('add_ratings', views.add_ratings, name='add_ratings'),
    path('search_names', views.search_names, name='search_names'),
    path('display_names', views.display_names, name='display_names'),
    #search_movie
    path('search_movie', views.search_movie, name='search_movie'),
    #display_movie_details
    path('display_movie_details', views.display_movie_details, name='display_movie_details')

]

