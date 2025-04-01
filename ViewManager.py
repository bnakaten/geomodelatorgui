# SPDX-FileCopyrightText: 2025 Benjamin Nakaten (GFZ) <bnakaten@gfz-potsdam.de>
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
#
# SPDX-License-Identifier: GPL-3.0-only

import pandas as pd
import streamlit as st

class ViewManager:
    gbs = {}

    def __init__(self):
        self.gb = st.session_state.GLOBALS

        self.setStructureColor('partition', 'partitionColor')
        self.setStructureColor('surface', 'surfaceColor')

        formViewManager = st.form('view')

        if 'zscale' not in st.session_state:
            st.session_state.zscale = 1

        if 'hide_inactive_cells' not in st.session_state:
            st.session_state.hide_inactive_cells = False

        if 'show_partitions' not in st.session_state:
            st.session_state.show_partitions = ''

        if 'partitionColor' not in st.session_state:
            st.session_state.partitionColor = ""

        if 'model_opacity' not in st.session_state:
            st.session_state.model_opacity = \
                self.gb.viewControl['modelOpacity']['default']

        if 'model_wireframe_opacity' not in st.session_state:
            st.session_state.model_wireframe_opacity = \
                self.gb.viewControl['modelWireframe']['default']

        if 'hide_model' not in st.session_state:
            st.session_state.hide_model = self.gb.viewControl['modelHide']['default']

        if 'show_surfaces' not in st.session_state:
            st.session_state.show_surfaces = 'all'

        if 'surfaceColor' not in st.session_state:
            st.session_state.surfaceColor = ""

        if 'structure_opacity' not in st.session_state:
            st.session_state.structure_opacity = \
                self.gb.viewControl['surfaceOpacity']['default']

        if 'structure_wireframe_opacity' not in st.session_state:
            st.session_state.structure_wireframe_opacity = \
                self.gb.viewControl['surfaceWireframe']['default']

        if 'hide_structure' not in st.session_state:
            st.session_state.hide_structure = \
                self.gb.viewControl['surfaceHide']['default']

        if 'plottercolor' not in st.session_state:
            st.session_state.plottercolor = \
                self.gb.viewControl['backgroundColor']['color']



        if not st.session_state.partitionColor.empty:

            formViewManager.slider(
                self.gb.viewControl['zAxisScale']['descriptionLable'],
                min_value = self.gb.viewControl['zAxisScale']['min'],
                max_value = self.gb.viewControl['zAxisScale']['max'],
                step = self.gb.viewControl['zAxisScale']['step'],
                help=self.gb.viewControl['zAxisScale']['help'],
                key = 'zscale',
                label_visibility="visible",
            )
            st.session_state.partitionColor = \
                st.session_state.partitionColor.style.apply(self.colorize, axis=1)

            st.session_state.partitionColor_e = formViewManager.data_editor(
                st.session_state.partitionColor,
                column_config={
                    "Partition": st.column_config.Column(disabled=True),
                    "Show": st.column_config.CheckboxColumn(),
                    "color": None,
                    "Id": st.column_config.Column(disabled=True)
                },
                hide_index = True,
                num_rows = 'fixed',
            )

            formViewManager.slider(
                self.gb.viewControl['modelOpacity']['descriptionLable'],
                min_value = self.gb.viewControl['modelOpacity']['min'],
                max_value = self.gb.viewControl['modelOpacity']['max'],
                step = self.gb.viewControl['modelOpacity']['step'],
                key = 'model_opacity'
            )

            c1, c2 = formViewManager.columns(2)
            c1.toggle(
                self.gb.viewControl['modelWireframe']['descriptionLable'],
                key = 'model_wireframe_opacity'
            )

            c2.toggle(
                self.gb.viewControl['modelHide']['descriptionLable'],
                key = 'hide_model'
            )
        else:
            st.session_state.partitionColor_e = False

        if not st.session_state.surfaceColor.empty:

            st.session_state.surfaceColor = st.session_state.surfaceColor.style.apply(
                self.colorize, axis=1
            )

            st.session_state.surfaceColor_e = formViewManager.data_editor(
                st.session_state.surfaceColor,
                column_config={
                    "Surface": st.column_config.Column(disabled=True),
                    "Show": st.column_config.CheckboxColumn(),
                    "color": None,
                    "Id": st.column_config.Column(disabled=True)
                },
                hide_index = True,
                num_rows = 'fixed',
            )

            formViewManager.slider(
                self.gb.viewControl['surfaceOpacity']['descriptionLable'],
                min_value = self.gb.viewControl['surfaceOpacity']['min'],
                max_value = self.gb.viewControl['surfaceOpacity']['max'],
                step = self.gb.viewControl['surfaceOpacity']['step'],
                key = 'structure_opacity'
            )

            c3, c4 = formViewManager.columns(2)
            c3.toggle(
                self.gb.viewControl['surfaceWireframe']['descriptionLable'],
                key = 'structure_wireframe_opacity'
            )

            c4.toggle(
                self.gb.viewControl['surfaceHide']['descriptionLable'],
                key = 'hide_structure'
            )
        else:
            st.session_state.surfaceColor_e = False

        pickedColor = formViewManager.color_picker(
            self.gb.viewControl['backgroundColor']['descriptionLable'],
            st.session_state.plottercolor,
        )

        st.session_state.show_e = formViewManager.form_submit_button(
            self.gb.button['show'],
            on_click=st.session_state.handler.btnShow,
            type="primary"
        )

        try:
            if st.session_state.show_e:
                if pickedColor:
                    st.session_state.plottercolor = pickedColor

                if 'surfaceColor_e' in st.session_state and \
                    not st.session_state.surfaceColor_e.empty:
                    st.session_state.configuration['surfaceColor'] = \
                        st.session_state.surfaceColor_e.to_dict('records')
                if 'partitionColor_e' in st.session_state and \
                    not st.session_state.partitionColor_e.empty:
                    st.session_state.configuration['partitionColor'] = \
                        st.session_state.partitionColor_e.to_dict('records')
        except:
            pass


    def colorize(self, color):
        return [
            f'background-color: {color.color}'
        ]*len(color) if color.color[0] == '#' else ['background-color: white']*len(color)

    def setStructureColor(self,structureName='partition',structureColor='partitionColor'):
        i = 0
        pnames = []
        pvalues = []
        pid = []
        pshow = []

        for id, part \
            in enumerate(st.session_state.configuration['gui'][structureColor]['color']):
            partitionName = \
                st.session_state.configuration['gui'][structureColor][structureName][i]
            pnames.append(partitionName)
            pvalues.append(part)
            try:
                pid.append(
                    st.session_state.configuration['model']["partitionId"][partitionName]
                )
            except:
                pid.append("-")

            pshow.append(st.session_state.configuration['gui'][structureColor]['show'][i])
            i += 1

        if structureName == 'partition':
            partitionColor = dict(Partition=pnames, color=pvalues, Id=pid, Show=pshow)

        if structureName == 'surface':
            partitionColor = dict(Surface=pnames, color=pvalues, Id=pid, Show=pshow)

        st.session_state[structureColor] = pd.DataFrame.from_dict(
            partitionColor,
            orient='index'
        ).transpose()