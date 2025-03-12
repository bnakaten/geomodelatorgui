import json
import streamlit as st

class GmlConnector:
    def __init__(self):
        self.serverConnection = True

        globals = st.session_state.GLOBALS

        if st.session_state.btnApiGmlRun:

            configuration = st.session_state.configuration
            configuration['config']['base'] = globals.default['uploadPath']

            configuration['config']['inputPath'] = ''
            configuration['config']['outputPath'] = ''
            configuration['config']['shapePath'] = ''


            errorMessage = False
            try:
                response = st.session_state.apiSession.post(
                    globals.default['apiBaseUrl'] + "configure",
                    json=json.dumps(configuration)
                )
            except:
                errorMessage = "Please, check the server. Start or restart it: ***python gmlPort.py***!" 
                st.error(errorMessage)
                self.serverConnection = False

            if errorMessage:
                print(errorMessage)
            else:
                response = st.session_state.apiSession.get(
                    globals.default['apiBaseUrl'] + "configuration"
                ).json()

                if not response:
                    print(response)
                else:
                    st.session_state.configuration = response

                    st.session_state.stateApiGmlConfigure = True

                    with st.spinner("Generate model ..."):
                        st.session_state.configuration = st.session_state.apiSession.get(
                            globals.default['apiBaseUrl'] + "run"
                        ).json()

                        if st.session_state.configuration['run']:
                            st.session_state.plot = True

                        st.session_state.stateApiGmlRun = True

        if st.session_state.stateApiGmlRun:
            st.session_state.plot = st.session_state.configuration['run']
