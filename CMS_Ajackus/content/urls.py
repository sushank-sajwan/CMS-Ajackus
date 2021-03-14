from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from knox import views as knox
from rest_framework.routers import DefaultRouter

from .views import (ContentCreateView, ContentDeleteView, ContentSearchView,
                    ContentUpdateView, ContentView)

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('fetch/', ContentView.as_view()),
    path('create/', ContentCreateView.as_view()),
    path('edit/<int:pk>/', ContentUpdateView.as_view()),
    path('delete/<int:pk>/', ContentDeleteView.as_view()),
    path('search/', ContentSearchView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
