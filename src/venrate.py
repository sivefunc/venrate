from dataclasses import dataclass, field
from typing import Dict

from platforms import (
        binance,
        bcv,
        yadio,
        monitordolar)

from _version import __version__

import exchange

@dataclass
class Venrate(exchange.Exchange):
    platforms: Dict = field(
        default_factory=lambda:{
            'BINANCE': binance.Binance(),
            'YADIO': yadio.Yadio(),
            'MONITORDOLAR': monitordolar.MonitorDolar(),
            'BCV': bcv.BCV(),
            }
        )

    def get_rate(self,
            platform: str,
            currency_from: str = None,
            currency_to: str = None,
            use_last_response=False,
            method: str = None,
            url: str = None,
            **kwargs) -> float:

        platform = platform.upper()
        if (platform_class := self.platforms.get(platform)) is None:
            platforms = self.platforms.keys()
            raise exchange.Exchange(
                    f"Platform {platform} not in {platforms}",
                    response=None)

        return platform_class.get_rate(
                currency_from = currency_from,
                currency_to = currency_to,
                method = method or self.method,
                url = url or self.url,
                use_last_response=use_last_response,
                **kwargs);

if __name__ == '__main__':
    venrate = Venrate()
    for p_name, platform in venrate.platforms.items():
        currency_from = platform.currency_from
        currency_to = platform.currency_to

        rate = venrate.get_rate(
                p_name,
                currency_from,
                currency_to,
                use_last_response=False,
                timeout=10,
                verify=True)

        print(f"{p_name} rate from '{currency_from}' to '{currency_to}' is"
                " " f"'{rate}'")
