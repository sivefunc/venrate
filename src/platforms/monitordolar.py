from dataclasses import dataclass

import requests

import exchange

@dataclass
class MonitorDolar(exchange.Exchange):
    method: str = "GET"
    url: str = "https://t.me/s/enparalelovzlatelegram"

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
                url = url or self.url,
                use_last_response=use_last_response,
                **kwargs)

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
                raise exchange.ExchangeError(
                        "No price (empty) found on </i> Bs. PRICE </br>"
                            " " "did Telegram or MonitorDolar has been changed?",
                        None)

            # MonitorDolar uses comma as decimal separator.
            try:
                price = float(price.replace(',', '.'))

            except Exception as error:
                raise exchange.ExchangeError(
                        f"Couldn't convert '{price}' to float", None) \
                    from error
            
        if price is None:
            raise exchange.ExchangeError(
                    "</i> Bs. PRICE </br> Not found on entire website"
                        " " "did Telegram or MonitorDolar changed the format?",
                    None
                    )

        self.last_response = response
        return price

if __name__ == '__main__':
    monitordolar = MonitorDolar()
    rate = monitordolar.get_rate('USD', use_last_response=False, timeout=10)
    print(f"MonitorDolar rate is: {rate}")
