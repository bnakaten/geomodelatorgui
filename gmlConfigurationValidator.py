import sys
import json
from jsonschema import Draft202012Validator

import importlib
gml = importlib.import_module("geomodelator-backend")

import logging
# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.basicConfig(stream=sys.stderr, level=logging.WARNING)


class gmlConfigurationValidator:

    def __init__(self, configurationDict):

        with open('gmlConfigurationJsonSchema.json', 'r') as file:
            jsonSchema = json.load(file)

            Draft202012Validator.check_schema(jsonSchema)
            draft_202012_validator = Draft202012Validator(jsonSchema)

            draft_202012_validator.is_valid(json.dumps(configurationDict))
            draft_202012_validator.validate(configurationDict)