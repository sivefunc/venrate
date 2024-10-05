import requests
from typing import Dict
from dataclasses import dataclass, field

class BCVerror(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

@dataclass
class BCV:
    url: str = "https://www.bcv.org.ve"
    currencies: list[str] = field(default_factory = lambda:
                                ['EUR', 'CNY', 'TRY', 'RUB', 'USD'])
    last_html: str = ""

    def get_currency(self,
                        currency: str,
                        use_last_html=False,
                        **kwargs) -> float:
        """
            parses BCV html page to get the price of a given currency on VEF.
            
            Args:
                currency     : ISO 4217 code, e.g: united states dollar is USD.
                                BCV only has EUR, CNY, TRY, RUB and USD.

                use_last_html: do not connect to internet, use the last html.

            Returns (SUCCESS):
                price of currency on VEF converted to float.
                and modifies self.last_html to the new html.

            Raises:
                BCVerror: These are due to html page changes or user.
                    1 - Currency not available
                    2 - <span>currency</span> not found
                    3 - <strong> opening tag not found
                    4 - </strong> closing tag not found
                    5 - price not found it's empty between tags.
                    6 - failed to convert price between tags.
        """
        if currency not in self.currencies:
            raise BCVerror(f"Currency {currency} not in available currencies: "
                            f"{self.currencies}")
        
        html = self.get_html(**kwargs) if not use_last_html else self.last_html
        if (span_idx := html.find(currency)) == -1:
            raise BCVerror(f"Couldn't find <span>{currency}</span>"
                            " " f"did html has been changed?")


        if (open_strong_idx := html.find("<strong>", span_idx)) == -1:
            raise BCVerror(f"Couldn't find opening tag <strong> of {currency}"
                            " " f"did html has been changed?")

        if (close_strong_idx := html.find("</strong>", open_strong_idx)) == -1:
            raise BCVerror(f"Couldn't find closing tag </strong> of {currency}"
                            " " f"did html has been changed?")
                            
        # Hopefully everything went well
        price = html[open_strong_idx + len('<strong>') : close_strong_idx]
        price = price.strip()
        if not price:
            raise BCVerror("No price (empty) found on <strong></strong>"
                            " " "did html has been changed?")
        try:
            price = float(price.replace(',', '.'))

        except Exception as error:
            raise BCVerror(f"Couldn't convert {currency} price to float: "
                            f"'{price}' did html has been changed?")
                            
        self.last_html = html
        return price # :) 

    def get_currencies(self, use_last_html=False, **kwargs) -> Dict[str, float]:
        """
            get_currency() on each of the currencies available
            {EUR, CNY, TRY, RUB, USD]

            Args:
                use_last_html: do not connect to internet, use the last html.

            Returns (SUCCESS):
                dict with all the currencies and their corresponding
                conversion on VEF.
                e.g
                    {'CNY' : 5.61811}

                and modifies self.last_html to the new html.

            Notes:
                1. get_currency().
        """
        html = self.get_html(**kwargs) if not use_last_html else self.last_html
        self.last_html = html

        currencies = dict()
        for currency in self.currencies:
            currencies[currency] = self.get_currency(
                                        currency,
                                        use_last_html=True,
                                        **kwargs)
        return currencies

    def get_html(self, **kwargs) -> str:
        req = requests.get(self.url, **kwargs)
        req.raise_for_status()
        html = req.text
        return html
