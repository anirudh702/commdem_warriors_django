"""commdem_warriors_backend URL Configuration

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
from django.urls import path,include
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_app/', include("user.urls")),
    path('commitment_app/', include("commitment.urls")),
    path('subscription_app/', include("subscription.urls")),
    path('designation_app/', include("designation.urls")),
    path('cities_app/', include("cities.urls")),
    path('income_app/', include("income.urls")),
    path('notifications_app/', include("notifications.urls")),
    path('referral_code_app/', include("referralCode.urls")),
    path('location_app/', include("location.urls")),
    path("graphql", GraphQLView.as_view(graphiql=True)),
]
