# SPDX-FileCopyrightText: 2025 Benjamin Nakaten (GFZ) <bnakaten@gfz-potsdam.de>
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
#
# SPDX-License-Identifier: GPL-3.0-only

import sys
import json
from jsonschema import Draft202012Validator

import importlib
gml = importlib.import_module("geomodelator")

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
