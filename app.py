import json
from typing import List

from apistar import App, Route, types, validators
from apistar.http import JSONResponse


# helpers

def _load_business_data():
    with open('mock_business_data.json') as f:
        businesses = json.loads(f.read())
        return {business["id"]: business for business in businesses}


businesses = _load_business_data()

# used for validation
VALID_COUNTRIES = set([business["country"]
                       for business in businesses.values()])
BUSINESS_NOT_FOUND = "Business not found"


# definition


class Business(types.Type):
    id = validators.Integer(allow_null=True)  # assign in POST
    company = validators.String(max_length=100)
    address = validators.String(max_length=200)
    city = validators.String(max_length=50)
    country = validators.String(enum=list(VALID_COUNTRIES))
    # Thought would be enough to set default to '', but got error, "May not be null".
    # So added "allow_null = True"
    post_code = validators.String(max_length=20, default='', allow_null=True)


# API methods
def list_businesses() -> List[Business]:
    return [Business(b[1]) for b in sorted(businesses.items())]


def create_business(b: Business) -> JSONResponse:
    b_id = len(businesses) + 1
    b.id = b_id
    businesses[b_id] = b
    return JSONResponse(Business(b), 201)


def get_business(b_id: int) -> JSONResponse:
    b = businesses.get(b_id)
    if not b:
        error = {'error': BUSINESS_NOT_FOUND}
        return JSONResponse(error, 404)
    return JSONResponse(Business(b), 200)


# ! TODO: check into - func not working in Postman, but test passing
def update_business(b_id: int, b: Business) -> JSONResponse:
    if not businesses.get(b_id):
        error = {'error': BUSINESS_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    b.id = b_id
    businesses[b_id] = b
    return JSONResponse(Business(b), status_code=200)


# ! TODO: check into - func not working in Postman, but test passing
def delete_business(b_id: int) -> JSONResponse:
    if not businesses.get(b_id):
        error = {'error': BUSINESS_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    del businesses[b_id]
    return JSONResponse({}, status_code=204)


routes = [
    Route('/', method='GET', handler=list_businesses),
    Route('/', method='POST', handler=create_business),
    Route('/{b_id}/', method='GET', handler=get_business),
    Route('/{b_id}/', method='PUT', handler=update_business),
    Route('/{b_id}/', method='DELETE', handler=delete_business),
]

app = App(routes=routes)

if __name__ == '__main__':
    app.serve("127.0.0.1", 5000, debug=True)
