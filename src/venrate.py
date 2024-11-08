from dataclasses import dataclass, field
from typing import Dict

from platforms import (
        binance,
        bcv,
        yadio,
        monitordolar)

from _version import __version__

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
            'bcv': bcv.BCV(),
            'yadio': yadio.Yadio(),
            'monitordolar': monitordolar.MonitorDolar()
            })

    def get_rate(self,
            platform,
            currency: str,
            use_last_request: bool = False,
            **kwargs):

        if (platform_class := self.platforms.get(platform)) is None:
            platforms = self.platforms.keys()
            raise VenrateError(f"Platform {platform} not in {platforms}")

        return platform_class.get_rate(
                currency, use_last_request, **kwargs);

if __name__ == '__main__':
    venrate = Venrate()
    for platform in venrate.platforms.keys():
        # Binance only does crypto.
        currency = 'USD' if platform != 'binance' else 'USDT'
        rate = venrate.get_rate(
                platform,
                currency,
                use_last_request=False,
                timeout=10,
                verify=False)

        print(f"{platform} rate is: {rate}") 
