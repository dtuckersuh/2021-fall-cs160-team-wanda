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
from django.urls import path, include
from core import views as views
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('login')),
    path('login/', views.loginUser, name="login"),
    path('users/register', views.register, name="register"),
    path('home/', views.home, name="home"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('tutors/', views.tutors, name="tutors"),
    path('users/<int:id>', views.user)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
