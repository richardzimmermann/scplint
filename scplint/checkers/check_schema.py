from logging import getLogger
from pathlib import Path
import json

from jsonschema import Draft7Validator, validators
from jsonschema.exceptions import ValidationError

logger = getLogger()

MSGS = {'E000': {'rule': 'Validation Error', 'msg': '{errors}'}}


def format_errors(errors: list) -> list:
    ''' Re-format the errors from JSONSchema.

    Args:
        errors (list): a list with error messages

    Returns:
        validation_errors (list): a re-formated list of error messages
    '''
    logger.debug('format jsonschema validation errors')
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


class CheckSchema():
    def __init__(self, report):
        logger.debug('initialize: check schema')
        self.report = report
        self.scp = report.scp
        self._verify_schema()

    def _verify_schema(self):
        ''' verifies the json schema of the scp '''
        logger.debug('verify scp schema')
        logger.debug(self.scp.scp)

        script_location = Path(__file__).absolute().parent
        file_location = f'{script_location}/../models/scp.json'
        schema = json.loads(open(file_location, 'r').read())

        try:
            Draft7ValidatorDefaults = extend_with_default(Draft7Validator)
            validator = Draft7ValidatorDefaults(schema)
            validator.validate(self.scp.scp)
            msg = 'SCP schema validation was successful.'

            logger.info(msg)
            return msg

        except ValidationError:
            errors = sorted(validator.iter_errors(self.scp.scp),
                            key=lambda error: error.path)

            for error in format_errors(errors):
                details = {'errors': error}
                self.report.add_error(MSGS, 'E000', details)
