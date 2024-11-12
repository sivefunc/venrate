from dataclasses import dataclass
import os.path

import requests

import exchange

@dataclass
class Yadio(exchange.Exchange):
    method: str = "GET"
    url: str = "https://api.yadio.io/rate"
    currency_from: str = "VES"
    currency_to: str = "USD"

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

        response = self.get_response(
                method = method or self.method,
                url = os.path.join(
                    url or self.url,
                    currency_from, currency_to),
                use_last_response=use_last_response,
                **kwargs)

        r_json = response.json()
        if (error_msg := r_json.get('error')) is not None:
            raise exchange.ExchangeError(error_msg, response)
        
        price = r_json['rate']
        self.last_response = response 
        return price

if __name__ == '__main__':
    yadio = Yadio()
    currency_from, currency_to = yadio.currency_from, yadio.currency_to
    rate = yadio.get_rate(
            currency_from,
            currency_to,
            use_last_response=False,
            timeout=10)

    print(f"Yadio rate from '{currency_from}' to '{currency_to}' is '{rate}'")
