from typing import Any, Protocol

from django.conf import settings
from django.utils.module_loading import import_string


class ChargerController(Protocol):
    def authorize(self, session: Any) -> bool:
        """Authorize a paid session with the station's charging controller."""


def get_charger_controller() -> ChargerController | None:
    controller_path = settings.CHARGER_CONTROLLER_CLASS
    if not controller_path:
        return None
    return import_string(controller_path)()
