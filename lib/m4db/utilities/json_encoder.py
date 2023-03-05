r"""
Some utility encoders for JSON.
"""

import decimal
import json


class DecimalEncoder(json.JSONEncoder):
    r"""
    Helper class to encode decimal values.
    """
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)
