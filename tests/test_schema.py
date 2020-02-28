import glob
import json
from collections import defaultdict
from typing import Dict, List

from jsonschema import Draft7Validator, validators
from jsonschema.exceptions import ValidationError
import pytest


def format_errors(errors: list) -> list:
    ''' Re-format the errors from JSONSchema.

    Args:
        errors (list): a list with error messages

    Returns:
        validation_errors (list): a re-formated list of error messages
    '''
    validation_errors = []

    for error in errors:
        if error.path:
            error_msg = f'{error.path.pop()}: {error.message}'
        else:
            error_msg = error.message

        validation_errors.append(error_msg)

    return validation_errors


def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS['properties']

    def set_defaults(validator, properties, instance, schema):
        for property, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(property, subschema["default"])

        for error in validate_properties(
                validator,
                properties,
                instance,
                schema,
        ):
            yield error

    return validators.extend(
        validator_class,
        {"properties": set_defaults},
    )


def run_json_schema(schema, example):
    try:
        Draft7ValidatorDefaults = extend_with_default(Draft7Validator)
        validator = Draft7ValidatorDefaults(schema)
        validator.validate(example)

    except ValidationError:
        errors = sorted(validator.iter_errors(example),
                        key=lambda error: error.path)
        error_msg = format_errors(errors)

        if error_msg:
            pytest.fail(json.dumps(error_msg))


def test_schemas():
    schemas = glob.glob('scplint/models/*.json')
    print(schemas)

    for schema in schemas:
        file = open(schema, 'r')
        file_content = file.read()
        file_json = json.loads(file_content)

        for example in file_json.get('examples', []):
            try:
                run_json_schema(file_json, example)

            except ValidationError as error:
                print(error)
                pytest.fail(error)
