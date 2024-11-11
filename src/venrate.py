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
            'binance': binance.Binance(),
            'bcv': bcv.BCV(),
            'yadio': yadio.Yadio(),
            'monitordolar': monitordolar.MonitorDolar()
            })

    def get_rate(self,
            platform: str,
            currency: str,
            use_last_response=False,
            method: str = None,
            url: str = None,
            **kwargs) -> float:

        if (platform_class := self.platforms.get(platform)) is None:
            platforms = self.platforms.keys()
            raise exchange.Exchange(
                    f"Platform {platform} not in {platforms}",
                    response=None)

        return platform_class.get_rate(
                currency,
                method=method or self.method,
                url=url or self.url,
                use_last_response=use_last_response,
                **kwargs);

if __name__ == '__main__':
    venrate = Venrate()
    for platform in venrate.platforms.keys():
        # Binance only does crypto.
        currency = 'USD' if platform != 'binance' else 'USDT'
        rate = venrate.get_rate(
                platform,
                currency,
                use_last_response=False,
                timeout=10,
                verify=True)

        print(f"{platform} rate is: {rate}") 
