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


class Business(types.Type):
    id = validators.Integer(allow_null=True)  # assign in POST
    company = validators.String(max_length=100)
    address = validators.String(max_length=200)
    city = validators.String(max_length=50)
    country = validators.String(enum=list(VALID_COUNTRIES))
    post_code = validators.String(max_length=20, default="")


# API methods
def list_businesses() -> List[Business]:
    pass


def create_business(business: Business) -> JSONResponse:
    pass


def get_business(business_id: int) -> JSONResponse:
    pass


def update_business(business_id: int, business: Business) -> JSONResponse:
    pass


def delete_business(business_id: int) -> JSONResponse:
    pass


routes = [
    Route('/', method='GET', handler=list_businesses),
    Route('/', method='POST', handler=create_business),
    Route('/{car_id}/', method='GET', handler=get_business),
    Route('/{car_id}/', method='PUT', handler=update_business),
    Route('/{car_id}/', method='DELETE', handler=delete_business),
]

app = App(routes=routes)


if __name__ == '__main__':
    app.serve("127.0.0.1", 5000, debug=True)
