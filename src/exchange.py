from dataclasses import dataclass
import requests

# ; -- /* // <!--
# I don't know if this is the best naming for this class, TODO: Rename it
# ; -- */ // -->

class ExchangeError(Exception):
    """Exchange Error
    """

    def __init__(self,
            message: str,
            response: requests.Response):

        self.message = message
        self.response = response

    def __str__(self):
        return self.message

@dataclass
class Exchange:
    method: str = None
    url: str = None
    last_response: requests.Response = None
    currency_from: str = None
    currency_to: str = None

    def get_rate(self,
            currency_from: str = None,
            currency_to: str = None,
            use_last_response=False,
            method: str = None,
            url: str = None,
            **kwargs) -> float:
        """ This function must be overwritten by child class
        """
        return self.get_response(
                method = method or self.method,
                url = url or self.url,
                use_last_response=use_last_response,
                **kwargs)

    def get_response(self,
            use_last_response=False,
            check_for_response_status=True,
            **kwargs):

        response = self.last_response if use_last_response else \
                    requests.request(**kwargs)

        if check_for_response_status:
            response.raise_for_status()

        return response
