import json
from typing import List

from apistar import App, Route, types, validators
from apistar.http import JSONResponse


# helpers

def _load_business_data():
    with open('mock_business_data.json') as f:
        bs = json.loads(f.read())
        return {b["id"]: b for b in bs}


bs = _load_business_data()
# used for validation
VALID_COUNTRIES = set([b["country"]
                       for b in bs.values()])
BUSINESSES_NOT_FOUND = "Business not found"

# definition

# API methods

# if __name__ == '__main__':
#     pass
