# SPDX-FileCopyrightText: 2025 Benjamin Nakaten (GFZ) <bnakaten@gfz-potsdam.de>
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
#
# SPDX-License-Identifier: GPL-3.0-only

import os
import time
import pandas as pd
import streamlit as st

from PIL import Image

from Globals import Globals
from SessionHandler import SessionHandler
from StreamlitStyler import StreamlitStyler
from GmlConnector import GmlConnector
from ModelPlotter import ModelPlotter
from Download import Download
from ModelParameter import ModelParameter
from ViewManager import ViewManager
from Wizard import Wizard


def main():
    st.session_state.handler = SessionHandler(globals=(Globals()))

    StreamlitStyler()

    gmlConnection = GmlConnector()

    if not gmlConnection.serverConnection:
        time.sleep(10)
        os._exit(0)
        st.stop()

    globals =st.session_state.GLOBALS
    if st.session_state.wizardWindow:
        if "stateApiGmlRun" in st.session_state and \
            not st.session_state.stateApiGmlRun and \
           "btnApiGmlRun" in st.session_state and not st.session_state.btnApiGmlRun:
            logo = Image.open(st.session_state.GLOBALS.default['logo'])
            st.image(logo)
            st.button(
                globals.button['wizard'],
                on_click=st.session_state.handler.btnApiWizardRun,
                args=['interrupted'],
                key='mainWizardBtn'
            )
        wizard = Wizard()
        wizard.windowNavigation()

        st.button(
            globals.button['show'],
            on_click=st.session_state.handler.btnShow,
            type="primary"
        )

    if not st.session_state.wizardWindow or \
        ("stateApiGmlRun" in st.session_state and st.session_state.stateApiGmlRun):
        with st.sidebar:
            logo = Image.open(st.session_state.GLOBALS.default['logo'])
            st.image(logo)
            tabMenu = st.tabs(st.session_state.tabs)

            with tabMenu[0]:
                ViewManager()

            with tabMenu[1]:
                ModelParameter(tabMenu[1])

            with tabMenu[2]:
                Download(tabMenu[2])

            st.divider()
            st.button(
                globals.button['wizard'],
                on_click=st.session_state.handler.btnApiWizardRun,
                key='secondWizardBtn'
            )

        if not st.session_state.wizardWindow:
            ModelPlotter()

        st.session_state.handler.reload()


if __name__ == "__main__":
    main()
