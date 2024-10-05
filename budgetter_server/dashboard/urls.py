from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('bank', views.BankViewSet)
router.register('account', views.AccountViewSet)
router.register('category', views.CategoryViewSet)
router.register('transaction', views.TransactionViewSet)
router.register('ofx', views.OFXUploadViewSet, basename="ofx")

urlpatterns = router.urls
