from typing import Dict
from dataclasses import dataclass, field

import requests

import exchange

@dataclass
class Binance(exchange.Exchange):
    method: str = "POST"
    url: str = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    currency_from: str = "VES"
    currency_to: str = "USDT"

    payload: Dict[str, str | int | list | bool] = field(
        default_factory=lambda:{
            "fiat": Binance.currency_from,
            "page": 1,
            "rows": 10,
            "order": "trade_count",
            "tradeType": "BUY",
            "asset": Binance.currency_to,
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

    def get_rate(self,
            currency_from: str = None,
            currency_to: str = None,
            use_last_response=False,
            method: str = None,
            url: str = None,
            **kwargs) -> float:

        currency_from = currency_from or self.currency_from
        currency_to = currency_to or self.currency_to

        if not currency_from.strip() or not currency_to.strip():
            raise exchange.ExchangeError(
                    f"Currency from '{currency_from}' AND"
                        " " f"Currency to '{currency_to}' must not be empty",
                    None)

        self.payload['fiat'] = currency_from
        self.payload['asset'] = currency_to

        response = self.get_response(
                method=method or self.method,
                url=url or self.url,
                use_last_response=use_last_response,
                json=self.payload,
                **kwargs)

        r_json = response.json()
        if not r_json['success'] or not r_json['data']:
            raise exchange.ExchangeError(
                    f"POST request Payload failed or not data\n"
                    f"JSON response: {r_json}", response)

        try:
            price = float(response.json()['data'][0]['adv']['price'])

        except Exception as error:
            raise exchange.ExchangeError(
                    f"No price found on JSON or couldn't convert\n"
                    f"JSON response: {r_json}", response) from error

        self.last_response = response
        return price

if __name__ == '__main__':
    binance = Binance()
    currency_from, currency_to = binance.currency_from, binance.currency_to
    rate = binance.get_rate(
            currency_from,
            currency_to,
            use_last_response=False,
            timeout=10)

    print(f"Binance rate from '{currency_from}' to '{currency_to}' is '{rate}'")
