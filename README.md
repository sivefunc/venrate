# bcv-api
bcv-api is a small (fast ?) python library that connects to
[BCV](https://www.bcv.org.ve) to parse html and get the current price of
currencies in VEF. 
<div align="center">
<img
    src="https://codeberg.org/Sivefunc/bcv-api/raw/branch/main/readme_res/logo.png"
    alt="bcv logo"
    width="200"
    height="200"/>
</div>

# Requeriments
- python3 >= 3.9
- requests >= 2.32.3
- dataclasses and typing (standard libraries)

# Using bcv-api.
<div align="center">
<img
    src="https://codeberg.org/Sivefunc/bcv-api/raw/branch/main/readme_res/exchange-rates.png"
    alt="exchange rates"
    width="200"
    height="200"/>
</div>

```python3
# importing BCV and creating object.
from bcv_api import BCV
bcv_con = BCV()

# Get a currency
eur = bcv_con.currencies[0]
print(eur, bcv_con.get_currency(eur))

# Get all currencies
for currency, price in bcv_con.get_currencies().items():
    print(currency, price)

# Use last html saved by get_currencies() to not use internet in this query.
cny = bcv_con.currencies[1]
print(cny, bcv_con.get_currency(cny, use_last_html=True))
```

# Installation
You can install BCV-api from [Pypi](https://pypi.org/project/bcv-api/)
```sh
pip install bcv-api
```

## Made by :link: [Sivefunc](https://gitlab.com/sivefunc)
## Licensed under :link: [GPLv3](https://codeberg.org/Sivefunc/bcv-api/src/branch/main/LICENSE)
