from dataclasses import dataclass

import requests

class YadioError(Exception):
    """Yadio json response related errors
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

@dataclass
class Yadio():
    url: str = "https://api.yadio.io/rate/VES/"
    last_response: requests.Response = None
    timeout: int = 10

    def get_rate(self, currency: str, use_last_response=False, **kwargs) -> float:

        if not currency.strip():
            raise YadioError("Currency must not be empty")

        if kwargs.get('timeout') is None:
            kwargs['timeout'] = self.timeout

        if not use_last_response:
            response = requests.get(f"{self.url}{currency}", **kwargs)
            response.raise_for_status()

        else:
            response = self.last_response

        r_json = response.json()
        if (error_msg := r_json.get('error')) is not None:
            raise YadioError(error_msg)
        
        price = r_json['rate']
        self.last_response = response 
        return price

if __name__ == '__main__':
    yadio = Yadio()
    rate = yadio.get_rate('USD', use_last_response=False, timeout=10)
    print(f"Yadio rate is: {rate}")
