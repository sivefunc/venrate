from dataclasses import dataclass

import requests

class MonitorDolarError(Exception):
    """MonitorDolar HTML response related errors
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

@dataclass
class MonitorDolar():
    url: str = "https://t.me/s/enparalelovzlatelegram"
    last_request: str = ""
    timeout: int = 10

    def get_rate(self, currency: str, use_last_req=False, **kwargs) -> float:
        if not currency.strip():
            raise MonitorDolarError("Currency must not be empty")

        if kwargs.get('timeout') is None:
            kwargs['timeout'] = self.timeout

        response = requests.get(self.url, **kwargs)
        response.raise_for_status()
        html = response.text
        price = None

        message_class = "tgme_widget_message_wrap"
        message_class_len = len(message_class)
        message_start_idx = - message_class_len
        while (message_start_idx := html.find(
                message_class,
                message_start_idx + message_class_len)) != -1:

            message_end_idx = html.find(
                    message_class,
                    message_start_idx + message_class_len)

            text_start_idx = html.find(
                    "tgme_widget_message_text", message_start_idx)

            if ((message_end_idx != -1 and text_start_idx > message_end_idx) or
                text_start_idx == -1):
                continue

            rate_start_idx = html.find("Bs.", text_start_idx)
            if (rate_start_idx == -1 or
                (message_end_idx != -1 and rate_start_idx > message_end_idx)):
                continue

            rate_end_idx = html.find("<br/>", rate_start_idx)
            if (rate_end_idx == -1 or
                (message_end_idx != -1 and rate_end_idx > message_end_idx)):
                continue

            price = html[rate_start_idx + len("Bs."):rate_end_idx].strip()
            
            if not price:
                raise MonitorDolarError(
                        "No price (empty) found on </i> Bs. PRICE </br>"
                        " " "did Telegram or MonitorDolar has been changed?")

            # MonitorDolar uses comma as decimal separator.
            try:
                price = float(price.replace(',', '.'))

            except Exception as error:
                raise MonitorDolarError(
                        f"Couldn't convert '{price}' to float") from error
            
        if price is None:
            raise MonitorDolarError(
                    "</i> Bs. PRICE </br> Not found on entire website"
                    " " "did Telegram or MonitorDolar changed the format?"
                    )

        return price
