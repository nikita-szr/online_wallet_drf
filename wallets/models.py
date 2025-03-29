from uuid import uuid4
from django.db import models


def generate_uuid():
    return str(uuid4())


class Wallet(models.Model):
    uuid = models.CharField(max_length=50, default=generate_uuid(), unique=True)
    balance = models.DecimalField(max_digits=30, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Кошелек {self.uuid} - Баланс: {self.balance} - Последняя операция: {self.last_update_at}'


class Transaction(models.Model):
    OPERATION_CHOICES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw')
    ]

    STATUS_CHOICES = [
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    operation_type = models.CharField(max_length=10, choices=OPERATION_CHOICES)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="SUCCESS")

    def __str__(self):
        return f"{self.operation_type} {self.amount} ({self.status})"
