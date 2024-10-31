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
    last_request: str = ""
    timeout: int = 10

    def get_currency(self,
            currency: str,
            use_last_request: bool = False,
            **kwargs):

        if not currency.strip():
            raise YadioError("Currency must not be empty")

        if kwargs.get('timeout') is None:
            kwargs['timeout'] = self.timeout

        response = requests.get(f"{self.url}{currency}", **kwargs)
        response.raise_for_status()
        r_json = response.json()
        if (error_msg := r_json.get('error')) is not None:
            raise YadioError(error_msg)
        
        price = r_json['rate']
        return price
