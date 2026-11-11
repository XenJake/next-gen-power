from typing import Any, Protocol

from django.conf import settings
from django.utils.module_loading import import_string


class PaymentProvider(Protocol):
    def create_checkout(self, payment: Any, request: Any) -> str:
        """Create a provider-hosted checkout and return its redirect URL."""

    def verify_webhook(self, request: Any) -> dict[str, Any] | None:
        """Verify provider signatures and return normalized event details."""


def get_payment_provider() -> PaymentProvider | None:
    provider_path = settings.PAYMENT_PROVIDER_CLASS
    if not provider_path:
        return None
    return import_string(provider_path)()
