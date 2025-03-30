import pytest
from rest_framework.test import APIClient
from rest_framework import status
from .models import Wallet, Transaction
from uuid import uuid4


@pytest.fixture
def wallet():
    return Wallet.objects.create(uuid=uuid4(), balance=1000)


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_wallet_creation(client):
    url = "/ow/api/v1/wallets/"
    data = {
        "balance": 1000,
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert "uuid" in response.data
    assert response.data["balance"] == "1000.00"


@pytest.mark.django_db
def test_wallet_list(client):
    Wallet.objects.create(uuid=uuid4(), balance=500)
    Wallet.objects.create(uuid=uuid4(), balance=1500)

    url = "/ow/api/v1/wallets/"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_wallet_not_found(client):
    url = "/ow/api/v1/wallets/non-existing-uuid/"
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_wallet_operation_deposit(client, wallet):
    url = f"/ow/api/v1/wallets/{wallet.uuid}/operation/"
    data = {
        "operation_type": "DEPOSIT",
        "amount": 500
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["balance"] == "1500.00"
    assert Transaction.objects.count() == 1
    assert Transaction.objects.first().status == "SUCCESS"


@pytest.mark.django_db
def test_wallet_operation_withdraw(client, wallet):
    url = f"/ow/api/v1/wallets/{wallet.uuid}/operation/"
    data = {
        "operation_type": "WITHDRAW",
        "amount": 500
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["balance"] == "500.00"
    assert Transaction.objects.count() == 1
    assert Transaction.objects.first().status == "SUCCESS"


@pytest.mark.django_db
def test_wallet_operation_insufficient_funds(client, wallet):
    url = f"/ow/api/v1/wallets/{wallet.uuid}/operation/"
    data = {
        "operation_type": "WITHDRAW",
        "amount": 1500
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Insufficient funds." in response.data["error"]
    assert Transaction.objects.count() == 1
    assert Transaction.objects.first().status == "FAILED"


@pytest.mark.django_db
def test_invalid_operation_type(client, wallet):
    url = f"/ow/api/v1/wallets/{wallet.uuid}/operation/"
    data = {
        "operation_type": "INVALID_OPERATION",
        "amount": 100
    }

    response = client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Неверный тип операции" in response.data["error"]
