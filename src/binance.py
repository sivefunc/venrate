from typing import Dict
from dataclasses import dataclass, field

import requests

class BinanceError(Exception):
    """Binance json response related errors
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

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
            currency: str,
            use_last_request: bool = False,
            **kwargs):

        if not currency.strip():
            raise BinanceError("Currency must not be empty")

        if kwargs.get('timeout') is None:
            kwargs['timeout'] = self.timeout

        self.payload['asset'] = currency
        response = requests.request(
                'POST',
                self.url,
                json=self.payload,
                **kwargs)

        response.raise_for_status()
        r_json = response.json()
        if not r_json['success'] or not r_json['data']:
            raise BinanceError(f"POST request Payload failed or not data\n"
                                f"JSON response: {r_json}")

        try:
            price = float(response.json()['data'][0]['adv']['price'])

        except Exception as error:
            raise BinanceError(f"No price found on JSON or couldn't convert\n"
                                f"JSON response: {r_json}") from error

        return price
