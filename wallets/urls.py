from django.urls import path
from .views import WalletListCreateView, WalletDetailView, WalletOperationView

app_name = "wallets"

urlpatterns = [
    path('api/v1/wallets/', WalletListCreateView.as_view(), name='wallet_list_create'),
    path("ow/api/v1/wallets/<uuid:uuid>/", WalletDetailView.as_view(), name="wallet-detail"),
    path('api/v1/wallets/<uuid:wallet_uuid>/operation/', WalletOperationView.as_view(), name='wallet_operation'),
]
