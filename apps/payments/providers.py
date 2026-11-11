from typing import Any, Protocol
import uuid

from django.conf import settings
from django.urls import reverse
from django.utils.module_loading import import_string


class PaymentProvider(Protocol):
    def create_checkout(self, payment: Any, request: Any) -> str:
        """Create a provider-hosted checkout and return its redirect URL."""

    def verify_webhook(self, request: Any) -> dict[str, Any] | None:
        """Verify provider signatures and return normalized event details."""


class MockPaymentProvider:
    """Local-only provider that records simulated payments without moving money."""

    def create_checkout(self, payment: Any, request: Any) -> str:
        return reverse('payments:mock_checkout', kwargs={'public_id': payment.public_id})

    def verify_webhook(self, request: Any) -> dict[str, Any] | None:
        return None

    def create_mock_reference(self) -> str:
        return f'MOCK-{uuid.uuid4().hex[:16].upper()}'


def get_payment_provider() -> PaymentProvider | None:
    provider_path = settings.PAYMENT_PROVIDER_CLASS
    if not provider_path or provider_path == 'disabled':
        return None
    return import_string(provider_path)()
