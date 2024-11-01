from dataclasses import dataclass, field
from typing import Dict

from platforms import (
        binance,
        bcv_api,
        yadio,
        monitordolar)

class VenrateError(Exception):
    """Venrate related
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

@dataclass
class Venrate:
    platforms: Dict = field(
        default_factory=lambda:{
            'binance': binance.Binance(),
            'bcv': bcv_api.BCV(),
            'yadio': yadio.Yadio(),
            'monitordolar': monitordolar.MonitorDolar()
            })

    def get_currency(self,
            platform,
            currency: str,
            use_last_request: bool = False,
            **kwargs):

        if (platform_class := self.platforms.get(platform)) is None:
            platforms = self.platforms.keys()
            raise VenrateError(f"Platform {platform} not in {platforms}")

        return platform_class.get_currency(
                currency, use_last_request, **kwargs);
