from django.urls import path
from .views import user_view, TokenView


urlpatterns = [
    path("", user_view, name='home'),
    path("login", TokenView.as_view(), name='login'),
]