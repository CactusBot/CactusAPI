from flask import request

from .rethink import get_one


def get_mixed_args(*args):
    request_args = request.values
    request_json = request.get_json()

    if request_json is None:
        data = request_args
    else:
        data = {**request_args, **request_json}

    data = {key: value for key, value in data.items() if key not in args}

    return data


def validate_data(model, data, partial=False):
    """
    Validates the provided data against the provided model
    Returns None if successful, a dict of errors if otherwise
    """
    errors = model.schema.validate(data, partial=partial)

    if errors != {}:
        return errors

    return None


def resource_exists(table_name, model, **kwargs):
    errors = validate_data(model, kwargs, True)
    if errors is not None:
        return errors, 400

    # Check if anything exists that exactly copies that
    exists = get_one(table_name, **kwargs)

    if exists == {}:
        return {}, 404

    return exists, None


def parse(model, data, partial=False):
    """Validates and dumps data into dict form"""

    data, errors = model.schema.load(data, partial=partial)

    if errors != {}:
        return {}, errors, 400

    dumped, errors = model.schema.dump(data)

    if errors != {}:
        return {}, errors, 400

    return dumped, {}, 200
