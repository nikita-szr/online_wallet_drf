from rest_framework import generics, status
from .models import Wallet, Transaction
from .serializers import WalletSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction


class WalletListCreateView(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletDetailView(generics.RetrieveDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = "uuid"


class WalletOperationView(APIView):
    def post(self, request, wallet_uuid):
        try:
            wallet = Wallet.objects.select_for_update().get(uuid=wallet_uuid)
            operation_type = request.data.get("operation_type")
            amount = request.data.get("amount")

            if operation_type not in ["DEPOSIT", "WITHDRAW"]:
                return Response({"error": "Неверный тип операции"}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                if operation_type == "WITHDRAW" and wallet.balance < amount:
                    Transaction.objects.create(wallet=wallet, operation_type=operation_type, amount=amount,
                                               status="FAILED")
                    return Response({"error": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)

                new_balance = wallet.balance + amount if operation_type == "DEPOSIT" else wallet.balance - amount
                wallet.balance = new_balance
                wallet.save()

                Transaction.objects.create(wallet=wallet, operation_type=operation_type, amount=amount,
                                           status="SUCCESS")
                return Response(WalletSerializer(wallet).data)

        except Wallet.DoesNotExist:
            return Response({"Ошибка": "Кошелек не найден"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"Ошибка": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
