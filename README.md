# venrate
Venrate is a library to get the exchange rate from currency A to currency B from different platforms like [BCV](https://www.bcv.org.ve).

<div align="center">
<img
    src="https://codeberg.org/Sivefunc/venrate/raw/branch/venrate/readme_res/logo.png"
    alt="venrate logo"
    width="200"
    height="100"/>
</div>

# Requeriments
- python3 >= 3.9
- requests >= 2.32.3
- dataclasses and typing (standard libraries)

# Installation
You can install venrate from [Pypi](https://pypi.org/project/venrate/)
```sh
pip install venrate
```

# Using venrate.
## Exchange rate from 'Bolivares' to 'US Dollars' in all platforms.
```python3
# importing venrate and creating object.
from venrate import Venrate
venrate = Venrate() 

for p_name, platform in venrate.platforms.items():
    currency_from = platform.currency_from
    currency_to = platform.currency_to

    rate = venrate.get_rate(
            p_name,
            currency_from,
            currency_to,
            use_last_response=False,
            timeout=10,                 # This is a requests.request option
            verify=True                 # This is a requests.request option
            )

    print(f"{p_name} rate from '{currency_from}' to '{currency_to}' is"
            " " f"'{rate}'")
```

## Exchange rate from 'Bolivares' to 'US Dollars' using BCV.
```python3
# importing venrate and creating object
from venrate import Venrate
venrate = Venrate()

platform_name = 'BcV' # Name is case insensitive
bcv_rate = venrate.get_rate(
            platform_name,
            use_last_response=False,
            timeout=10,
            verify=False            # Lately BCV it's giving SSL errors
            )

print(bcv_rate)

# Successfull requests.Response are saved, so you can use it later.
bcv_rate = venrate.get_rate(
            platform_name,
            use_last_response=True,
            timeout=10,
            verify=False            # Lately BCV it's giving SSL errors
            )

print(bcv_rate)
```

## Default currency names that platforms uses
```python3
# importing venrate and creating object
from venrate import Venrate
venrate = Venrate()

for p_name, platform in venrate.platforms.items():
    currency_from = platform.currency_from
    currency_to = platform.currency_to
    print(p_name, currency_from, currency_to)

# Why know this?
# Platforms could have different naming for currencies
# Binance for example uses USDT
# MonitorDolar, BCV and Yadio uses USD
```

# :notebook: Notes <a name="notes"></a>
- It's still a very premature library, it lacks:
    - Documentation
    - Tests
    - More platforms
    - More methods or new idea of superclass that results useful to use.

- There are platforms like MonitorDolar that only does BS to USD so if you try using different currencies or different ordering it will throw the same rate.

# Supported platforms
<table>
    <tr>
        <td>Name</td>
        <td>Image</td>
    </tr>
    <tr>
        <td>Binance</td>
        <td><img src="https://codeberg.org/Sivefunc/venrate/raw/branch/venrate/readme_res/binance.png" width="100" height="100"></td>
    </tr>
    <tr>
        <td>BCV</td>
        <td><img src="https://codeberg.org/Sivefunc/venrate/raw/branch/venrate/readme_res/bcv.png" width="100" height="100"></td>
    </tr>
    <tr>
        <td>MonitorDolar</td>
        <td><img src="https://codeberg.org/Sivefunc/venrate/raw/branch/venrate/readme_res/monitordolar.png" width="100" height="100"></td>
    </tr>
    <tr>
        <td>Yadio</td>
        <td><img src="https://codeberg.org/Sivefunc/venrate/raw/branch/venrate/readme_res/yadio.png" width="100" height="100"></td>
    </tr>
 </table>

# Made by :link: [Sivefunc](https://gitlab.com/sivefunc)
# Licensed under :link: [GPLv3](https://codeberg.org/Sivefunc/venrate/src/branch/main/LICENSE)
