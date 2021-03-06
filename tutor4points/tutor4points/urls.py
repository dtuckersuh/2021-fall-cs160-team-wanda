"""tutor4points URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from core import views as views
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('login/', views.loginUser, name="login"),
    path('users/register', views.register, name="register"),
    path('points/', views.points, name="points"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('tutors/', views.tutors, name="tutors"),
    path('users/<int:id>', views.users, name="user"),  ## User Profile Page
    path ('users/<int:id>/requests', views.requests, name = "requests"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
