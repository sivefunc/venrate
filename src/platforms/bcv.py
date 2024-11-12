"""Consult exchanges rates from BCV

This is the file that contains BCV and BCVError and handles everything
related to GET request BCV website and Parse the corresponding HTML page
to obtain the different exchanges rates that the website has.
"""

# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
from typing import Dict
from dataclasses import dataclass, field

import requests

import exchange

# -----------------------------------------------------------------------------
# Handmade code
# -----------------------------------------------------------------------------
@dataclass
class BCV(exchange.Exchange):
    """Extract information from BCV
    """

    method: str = "GET"
    url: str = "https://www.bcv.org.ve"
    currency_from: str = "VES"
    currency_to: str = "USD"

    def get_rate(self,
                currency_from: str = None,
                currency_to: str = None,
                use_last_response=False,
                method: str = None,
                url: str = None,
                **kwargs) -> float:
        """GET currency exchange rate to VEF.
        
        GET request to BCV (Banco Central de Venezuela) website to
        obtain the html page and then parse it to have the exchange
        rate of currency to VEF. 
        
        The parsing is done by considering this order of events:
        <span>Currency</span>
        <strong>Price</strong>
        
        Args:
            currency_to:
                ISO 4217 code, e.g: united states dollar is USD.
                BCV only has EUR, CNY, TRY, RUB and USD.

            use_last_response:
                do not connect to internet, use the last response as cache.

            **kwargs:
                Positional arguments for the requests.get method, e.g:
                timeout=10.

        Returns:
            A float that is the exchange rate of currency to VEF.
            and modifies self.last_response to the new success response.

        Raises:
            exchange.ExchangeError:
                Parsing error due to GET response html page changes or
                user.

                There is the GET response status 204 [No Content] that
                may raise this exception (empty text)

            HTTPError:
                Errors in range(400 <= x < 600) there are others errors
                related to Requests library that you must handle
                yourself, like timeout.

                <https://docs.python-requests.org/en/latest/_modules/requests/exceptions/>
                <https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module#16511493>
        """

        currency_from = currency_from or self.currency_from
        currency_to = currency_to or self.currency_to

        if not currency_from.strip() or not currency_to.strip():
            raise exchange.ExchangeError(
                    f"Currency from '{currency_from}' AND"
                        " " f"Currency to '{currency_to}' must not be empty",
                    None)

        response = self.get_response(
                method = method or self.method,
                url = url or self.url,
                use_last_response=use_last_response,
                **kwargs)

        html = response.text

        currency = currency_to
        # <span>Currency</span>
        if (span_idx := html.find(currency)) == -1:
            raise exchange.ExchangeError(
                    f"Couldn't find <span>{currency}</span>"
                        " " f"did html has been changed?", response)

        # <strong> after <span>
        if (open_strong_idx := html.find("<strong>", span_idx)) == -1:
            raise exchange.ExchangeError(
                    f"Couldn't find opening tag <strong> of {currency}"
                        " " f"did html has been changed?", response)

        # </strong> after <strong>
        if (close_strong_idx := html.find("</strong>", open_strong_idx)) == -1:
            raise exchange.ExchangeError(
                    f"Couldn't find closing tag </strong> of {currency}"
                        " " f"did html has been changed?", response)

        # Hopefully everything went well
        # <strong> Price </strong>
        price = html[open_strong_idx + len('<strong>') : close_strong_idx]
        price = price.strip()

        # <strong></strong>
        if not price:
            raise exchange.ExchangeError(
                    "No price (empty) found on <strong></strong>"
                        " " "did html has been changed?", response)

        # BCV uses comma as decimal separator.
        try:
            price = float(price.replace(',', '.'))

        except Exception as error:
            raise exchange.ExchangeError(
                    f"Couldn't convert {currency} price to float: "
                        f"'{price}' did html has been changed?",
                    response) from error

        # Everything went well, cache the result.
        self.last_response = response
        return price # :)

if __name__ == '__main__':
    bcv = BCV()
    currency_from, currency_to = bcv.currency_from, bcv.currency_to
    rate = bcv.get_rate(
            currency_from,
            currency_to,
            use_last_response=False,
            timeout=10, verify=False)

    print(f"BCV rate from '{currency_from}' to '{currency_to}' is '{rate}'")

# (1 + 3 + 5 + 7 + 9 + ... + n) = (n**2 + 2 - 1) // 2
