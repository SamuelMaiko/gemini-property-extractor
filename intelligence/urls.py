from django.urls import path
from .views import ExtractionView, ChatView

urlpatterns = [
    path('extract/', ExtractionView.as_view(), name='extract'),
    path('chat/', ChatView.as_view(), name='chat'),
]
