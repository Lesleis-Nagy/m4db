r"""
A selection of utility functions to check for simple data format consistency.
"""

import re

from m4db.decorators import static

@static(regex_decimal=re.compile(r"([0-9]+)(\.(([0-9])+)?)?"))
def is_str_decimal(str_decimal: str) -> bool:
    self = is_str_decimal
    if self.regex_decimal.match(str_decimal):
        return True
    else:
        return False
