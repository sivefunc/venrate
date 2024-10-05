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

# -----------------------------------------------------------------------------
# Handmade code
# -----------------------------------------------------------------------------
class BCVerror(Exception):
    """Parsing related errors

    Raises:
        Currency not available:
            Currency not in BCV.currencies
            This is the only not related to parsing by itself, because
            it does not look up in the HTML.

        <span>currency</span> not found:
            The BCV page (at least on 2024) each currency price came
            preceded by that line.

        <strong> opening tag not found:
            Price is between <strong> and </strong>

        </strong> closing tag not found:
            Price is between <strong> and </strong>
        
        Price not found:
            <strong></strong> Empty between tags.

        Failed to convert price between tags:
            The html could have changed and the text doesn't have text
            like '1,43' instead it's '1.ABC'
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

@dataclass
class BCV:
    """Extract information from BCV

    Attributes:
        url:
            String Address to GET request the html price.

        currencies:
            List of available currencies that can be consulted.

        last_html:
            String cache for future requests.
    """

    url: str = "https://www.bcv.org.ve"
    currencies: list[str] = field(default_factory = lambda:
                                ['EUR', 'CNY', 'TRY', 'RUB', 'USD'])
    last_html: str = ""

    def get_currency(self,
                        currency: str,
                        use_last_html=False,
                        **kwargs) -> float:
        """GET currency exchange rate to VEF.
        
        GET request to BCV (Banco Central de Venezuela) website to
        obtain the html page and then parse it to have the exchange
        rate of currency to VEF. 
        
        The parsing is done by considering this order of events:
        <span>Currency</span>
        <strong>Price</strong>
        
        Args:
            currency:
                ISO 4217 code, e.g: united states dollar is USD.
                BCV only has EUR, CNY, TRY, RUB and USD.

            use_last_html:
                do not connect to internet, use the last html as cache,
                also you can use this in the case of creating your own
                get_html() function, this way you 'bypass' the library
                own method of getting HTML.

            **kwargs:
                Positional arguments for the requests.get method, e.g:
                timeout=10.

        Returns:
            A float that is the exchange rate of currency to VEF.
            and modifies self.last_html to the new html.

        Raises:
            BCVerror:
                Parsing error due to GET response html page changes or
                user.

                There is the GET response status 204 [No Content] that
                may raise this exception (empty text -> get_html())

            HTTPError:
                Errors in range(400 <= x < 600) there are others errors
                related to Requests library that you must handle
                yourself, like timeout.

                <https://docs.python-requests.org/en/latest/_modules/requests/exceptions/>
                <https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module#16511493>
        """

        # Currency is not on the list.
        if currency not in self.currencies:
            raise BCVerror(f"Currency {currency} not in available currencies: "
                            f"{self.currencies}")

        html = self.get_html(**kwargs) if not use_last_html else self.last_html
        # <span>Currency</span>
        if (span_idx := html.find(currency)) == -1:
            raise BCVerror(f"Couldn't find <span>{currency}</span>"
                            " " f"did html has been changed?")

        # <strong> after <span>
        if (open_strong_idx := html.find("<strong>", span_idx)) == -1:
            raise BCVerror(f"Couldn't find opening tag <strong> of {currency}"
                            " " f"did html has been changed?")

        # </strong> after <strong>
        if (close_strong_idx := html.find("</strong>", open_strong_idx)) == -1:
            raise BCVerror(f"Couldn't find closing tag </strong> of {currency}"
                            " " f"did html has been changed?")

        # Hopefully everything went well
        # <strong> Price </strong>
        price = html[open_strong_idx + len('<strong>') : close_strong_idx]
        price = price.strip()

        # <strong></strong>
        if not price:
            raise BCVerror("No price (empty) found on <strong></strong>"
                            " " "did html has been changed?")

        # BCV uses comma as decimal separator.
        try:
            price = float(price.replace(',', '.'))

        except Exception as error:
            raise BCVerror(f"Couldn't convert {currency} price to float: "
                            f"'{price}' did html has been changed?") from error

        # Everything went well, cache the result.
        self.last_html = html
        return price # :)

    def get_currencies(self, use_last_html=False, **kwargs) -> Dict[str, float]:
        """GET BCV currencies exchange rates to VEF.

        get_currency() on each of the currencies listed on BCV.
        {EUR, CNY, TRY, RUB, USD}

        Args:
            use_last_html:
                do not connect to internet, use the last html as cache.

            **kwargs:
                Positional arguments for the requests.get method, e.g:
                timeout=10.

        Returns:
            Dict with all the currencies and their corresponding
            conversion rate to VEF.
            e.g:
                {'EUR': 40.60419933,
                 'CNY': 5.27755927,
                 'TRY': 1.08164956,
                 'RUB': 0.38848062,
                 'USD': 37.0358}

            and modifies self.last_html to the new html.

        Raises:
            BCVError: Parsing error.
            HTTPError: 400 <= x < 600

        Notes:
            get_currency():
                This is the function in 'singular' it explains on detail
                things like Raises or code internally.
        """
        html = self.get_html(**kwargs) if not use_last_html else self.last_html
        self.last_html = html

        currencies = {}
        for currency in self.currencies:
            currencies[currency] = self.get_currency(
                                        currency,
                                        use_last_html=True,
                                        **kwargs)
        return currencies

    def get_html(self, **kwargs) -> str:
        """GET request to BCV to obtain the HTML.
        
        Args:
            **kwargs:
                Positional arguments for the requests.get method, e.g:
                timeout=10.

        Returns:
            String containing html code, could be empty due to status
            code like 204 [No content].

        Raises:
            HTTPError:
                Errors in range(400 <= x < 600) there are others errors
                related to Requests library that you must handle
                yourself, like timeout.

                <https://docs.python-requests.org/en/latest/_modules/requests/exceptions/>
                <https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module#16511493>

        """

        req = requests.get(self.url, **kwargs)
        req.raise_for_status()
        html = req.text
        return html

# (1 + 3 + 5 + 7 + 9 + ... + n) = (n**2 + 2 - 1) // 2
