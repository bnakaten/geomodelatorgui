# SPDX-FileCopyrightText: 2025 Benjamin Nakaten (GFZ) <bnakaten@gfz-potsdam.de>
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
#
# SPDX-License-Identifier: GPL-3.0-only

import secrets
from flask import Flask, request, json, session
import gmlConfigurationMapper as gmlConfigMapper
import gmlConfigurationValidator as gmlConfigValidator
from gmlRunMapper import gmlRunMapper as gmlRunMapper


def main():
    APP = create_app()
    APP.run(debug=False)


def create_app(test_config=None):
    app = Flask(__name__)

    app.secret_key = secrets.token_hex()

    @app.route("/api/gml/configure", methods=['POST'])
    def gmlConfigureAdapter():

        app.secret_key = secrets.token_hex()

        responseString = json.loads(request.data)
        responseDict = json.loads(responseString)
        gmlConfigValidator.gmlConfigurationValidator(responseDict)

        if 'gml' in session:
            session.pop('gml')

        session['gml'] = (gmlConfigMapper.gmlConfigurationMapper(responseString)).rs

        return session['gml']


    @app.route("/api/gml/configuration", methods=['GET'])
    def gmlGetConfigruation():
        if "gml" not in session:
            data = '{"error": "No configuration data"}'
        else:
            data = session['gml']

        return data


    @app.route("/api/gml/run", methods=['GET'])
    def gmlRunService():
        if "gml" not in session:
            data = '{"error": "No configuration data"}'
        else:
            config = gmlConfigMapper.gmlConfigurationMapper(session['gml'])
            config.configureModel()

            gmlConfigValidator.gmlConfigurationValidator(config.rs)

            run = gmlRunMapper(config)
            session['gml'] = run.generateModel()
            data = session['gml']
            print(data)

        return json.dumps(data)

    return app


# if __name__ == '__main__':
#     import cProfile
#     import pstats
#     prof = cProfile.Profile()
#     prof.run("main()")
#     prof.dump_stats('backend_output.prof')

#     stream = open('backend_output.txt', 'w')
#     stats = pstats.Stats('backend_output.prof', stream=stream)
#     stats.sort_stats('cumtime')
#     stats.print_stats()

if __name__ == '__main__':
    main()