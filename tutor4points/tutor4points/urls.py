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

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_user, name="login"),
    path('register/', views.register, name="register"),
    path('register2/', views.register2, name="register2"),
    path('update-tutor-profile/', views.update_tutor_profile,
         name="update_tutor_profile"),
    path('dashboard/', views.dashboard,
         name="dashboard"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
