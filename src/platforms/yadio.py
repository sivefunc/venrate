from dataclasses import dataclass

import requests

import exchange

@dataclass
class Yadio(exchange.Exchange):
    method: str = "GET"
    url: str = "https://api.yadio.io/rate/VES/"

    def get_rate(self,
            currency: str,
            use_last_response=False,
            method: str = None,
            url: str = None,
            **kwargs) -> float:

        if not currency.strip():
            raise exchange.ExchangeError("Currency must not be empty", None)

        response = self.get_response(
                method = method or self.method,
                url = f"{url or self.url}{currency}",
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
    rate = yadio.get_rate('USD', use_last_response=False, timeout=10)
    print(f"Yadio rate is: {rate}")
