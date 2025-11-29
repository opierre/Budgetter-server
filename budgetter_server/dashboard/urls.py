from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('bank', views.BankViewSet)
router.register('account', views.AccountViewSet)
router.register('category', views.CategoryViewSet)
router.register('transaction', views.TransactionViewSet)

urlpatterns = [
    path('import/', views.import_ofx, name='import_ofx'),
    path('import/preview/', views.preview_import, name='preview_import'),
] + router.urls
