""" Befor first streamlit output element """
import streamlit as st

class StreamlitStyler:

    def __init__(self,
    ) -> None:

        aboutText = '''# GeomodelatorGUI

Graphical User interface (GUI) based on python, streamlit and pyvista for
[GEOMODELATOR](https://git.gfz.de/bnakaten/geomodelator), which allows to grid
and parametrise static 3D geolocial models for dynamic simulators
(e.g. TRANS[TRANSPORTSE](https://git.gfz.de/kempka/transportse)PORTSE).
'''
        ###### global streamlit inititalisation
        st.set_page_config(
            page_title='GeomodelatorGUI',
            page_icon='G',
            layout='wide',
            initial_sidebar_state='auto',
            menu_items={
                'Get Help': 'https://git.gfz.de/bnakaten/geomodelator/-/wikis/home',
                'Report a bug': 'mailto:bnakaten@gfz.de',
                'About': aboutText
            }
        )

        st.markdown(""" <style>
        .css-z5fcl4 {
        width: 100%;
        padding: 0;
        min-width: auto;
        max-width: initial;
        }
        .css-1544g2n { padding: 2rem 1rem 1.5rem;}
        .st-emotion-cache-1y4p8pa {
            max-width: none;
        }
        </style> """, unsafe_allow_html=True)