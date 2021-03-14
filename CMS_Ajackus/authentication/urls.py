from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AdminImportView, LoginView, UserImportTemplateView,
                    UserRegistrationView)

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='knox_login'),
    path('user_import_template/', UserImportTemplateView.as_view()),
    path('seed_admin/', AdminImportView.as_view()),
    path('register/', UserRegistrationView.as_view()),
]
