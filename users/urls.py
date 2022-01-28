from django.urls import path
from .views import TokenView, ProtectedView, not_protected_view, Not_ProtectedView


urlpatterns = [
    path("login", TokenView.as_view(), name='login'),
    path("protected_view", ProtectedView.as_view(), name='protected_view'),
    # path("not-protected_view", Not_ProtectedView.as_view(), name='not_protected_view'),
    path("not_protected_view", not_protected_view, name='not_protected_view')
]