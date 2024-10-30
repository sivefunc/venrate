from typing import Dict
from dataclasses import dataclass, field

import requests

@dataclass
class Binance():
    payload: Dict[str, str | int | list | bool] = field(
        default_factory=lambda:{
            "fiat": "VES",
            "page": 1,
            "rows": 10,
            "order": "trade_count",
            "tradeType": "BUY",
            "asset": "USDT",
            "countries": [],
            "proMerchantAds": False,
            "shieldMerchantAds": False,
            "filterType": "all",
            "periods": [],
            "additionalKycVerifyFilter": 0,
            "publisherType": "merchant",
            "payTypes": [],
            "classifies": ["mass","profession","fiat_trade"]
        })

    url: str = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    last_request: str = ""
    timeout: int = 10

    def get_currency(self,
            currency: str = "USDT",
            use_last_request: bool = True,
            **kwargs):

        if kwargs.get('timeout') is None:
            kwargs['timeout'] = self.timeout

        response = requests.request(
                'POST',
                self.url,
                json=self.payload,
                **kwargs)

        response.raise_for_status()
        return float(response.json()['data'][0]['adv']['price'])
