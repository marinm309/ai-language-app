from django.urls import path
from .views import AIChatAPIView

urlpatterns = [
    path("chat/", AIChatAPIView.as_view(), name="chat"),
]
