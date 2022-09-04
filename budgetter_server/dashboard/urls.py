from rest_framework.routers import DefaultRouter

from budgetter_server.dashboard import views

router = DefaultRouter()

router.register('bank', views.BankViewSet)
router.register('account', views.AccountViewSet)
router.register('category', views.CategoryViewSet)
router.register('transactions', views.TransactionViewSet)

urlpatterns = router.urls
