import os
import sys
import numpy
import streamlit as st
import pyvista
from stpyvista import stpyvista

from stpyvista.utils import start_xvfb
if "IS_XVFB_RUNNING" not in st.session_state:
  start_xvfb()
  st.session_state.IS_XVFB_RUNNING = True

numpy.set_printoptions(threshold=sys.maxsize)

class ModelPlotter:
    def __init__(self):
        globals = st.session_state.GLOBALS
        modelPathFileVtk = globals.default['uploadPath'] + \
            st.session_state.configuration['config']['outputPath'] + \
            st.session_state.configuration['config']['modelFileVtk']

        if st.session_state.plot and os.path.exists(modelPathFileVtk):
            with st.spinner(globals.ModelPlotter['loadingSpinnerText']):

                pyvista.start_xvfb()
                pyvista.global_theme.allow_empty_mesh = True
                pyvista.global_theme.colorbar_horizontal.width = \
                    globals.ModelPlotter['legendColorbar']

                self.plotter = pyvista.Plotter(window_size = [
                    globals.ModelPlotter['width'],
                    globals.ModelPlotter['height']
                ])

                self.plotter.set_background(st.session_state.plottercolor)

                mesh = pyvista.read(modelPathFileVtk)

                inactiveElements = (mesh.cell_data['active'] == 1).any()

                cmap, selectedPartitions = self.getPartitionsAndCmap(inactiveElements)

                mesh, structureOpacity = self.getMeshByListOfSelectedPartitions(
                    mesh, selectedPartitions, inactiveElements
                )

                mesh, modelOpacity = self.getPlotterWithSelectedSurfaces(
                    mesh, structureOpacity
                )

                if len(selectedPartitions) == 0:
                    mesh = mesh.extract_feature_edges()

                sargs = dict(
                    title='All partitions',
                    title_font_size=20,
                    label_font_size=16,
                    n_labels=5,
                    n_colors=5,
                    italic=True,
                    fmt="%.1f",
                )

                try:
                    self.plotter.add_mesh(
                        mesh,
                        scalars = 'all',
                        cmap = cmap,
                        lighting = False,
                        opacity = modelOpacity,
                        show_edges = st.session_state.model_wireframe_opacity,
                        scalar_bar_args=sargs,
                    )
                except:
                    mesh = mesh.extract_feature_edges()
                    self.plotter.add_mesh(
                        mesh,
                        cmap = cmap,
                        lighting = False,
                        opacity = modelOpacity,
                        show_edges = st.session_state.model_wireframe_opacity,
                        scalar_bar_args=sargs,
                    )


                self.plotter.show_axes()

                self.plotter.view_isometric()

                try:
                    stpyvista(
                        self.plotter,
                        panel_kwargs=dict(
                            orientation_widget=True, interactive_orientation_widget=True
                        )
                    )

                except:
                    st.error(globals.ModelPlotter['error']['plotterData'])

                st.info(globals.ModelPlotter['infoTextNavigation'], icon="ℹ️")

        elif st.session_state.plot:
            st.warning(
                globals.ModelPlotter['error']['somethingHasGoneWrong'] + ' \"' + \
                st.session_state.GLOBALS.default['uploadPath'] + \
                st.session_state.configuration['config']['outputPath'] + \
                st.session_state.GLOBALS.default['modelFileVtk'] + '\" ' + \
                globals.ModelPlotter['error']['couldNotbeFound'],
                icon="⚠️"
            )


    def getMeshByListOfSelectedPartitions(self, mesh, selectedPartitions, inactiveElements):
        if len(selectedPartitions) > 0 or (mesh.cell_data['active'] == 1).all():#and not inactiveElements:#and selectedPartitions[0] != 'default':
            t_cell_data = numpy.zeros_like(mesh.cell_data['all'])

            for part in selectedPartitions:
                t_cell_data[
                    mesh.cell_data['all'] == \
                        st.session_state.configuration['model']['partitionId'][part]
                ] = 1

            mesh.cell_data['threshold'] = t_cell_data
            mesh = mesh.threshold(value=[1,1], scalars="threshold")

        else:
            if mesh.cell_data['active'].any() == 0:
                t_cell_data = numpy.ones_like(mesh.cell_data['all'])
                t_cell_data[mesh.cell_data['active'] == 0] = 0

                mesh.cell_data['threshold'] = t_cell_data
                mesh = mesh.threshold(value=[1,1], scalars="threshold")


        mesh = mesh.scale([1,1,st.session_state.zscale])

        if st.session_state.hide_structure:
            structureOpacity = 0
        else:
            structureOpacity = st.session_state.structure_opacity

        return mesh, structureOpacity


    def getPlotterWithSelectedSurfaces(self, mesh, structureOpacity):

        df = st.session_state.surfaceColor_e
        i = 0

        for i, file in enumerate(
            st.session_state.configuration['structure']['file']
        ):
            if 'layer' == st.session_state.configuration['structure']['type'][i]\
                or \
                'fault' == st.session_state.configuration['structure']['type'][i]\
                or\
                'mask' == st.session_state.configuration['structure']['type'][i]:

                if file.split('.')[0] in st.session_state.show_surfaces or \
                    df.loc[df['Surface'] == file.split('.')[0],'Show'].values[0]:

                    try:
                        surface_data = pyvista.read(
                            st.session_state.GLOBALS.default['uploadPath'] + \
                            st.session_state.configuration['config']['outputPath'] + \
                            file.split('.')[0] + ".vtk"
                        )

                        tmp = []
                        for point in surface_data.points:
                            tmp.append(point[2])

                        surface_data.point_data['elevation'] = tmp
                        surface = surface_data.scale([1,1,st.session_state.zscale])

                        df = st.session_state.surfaceColor_e
                        self.plotter.add_mesh(
                            surface,
                            color = \
                                df.loc[
                                    df['Surface']==file.split('.')[0],'color'
                                ].values[0],
                            opacity = structureOpacity,
                            show_edges = \
                                st.session_state.structure_wireframe_opacity
                        )

                    except:
                        pass

                    i += 1

        if st.session_state.hide_model:
            modelOpacity = 0
        else:
            modelOpacity = st.session_state.model_opacity

        return mesh, modelOpacity


    def getPartitionsAndCmap(self, inactiveElements):
        cmap = []
        df = st.session_state.partitionColor_e

        selectedPartitions = []
        for part in st.session_state.configuration['gui']['partitionColor']['partition']:

            if df.loc[df['Partition'] == part,'Show'].values[0]:
                color = df[df['Partition'] == part]

                cmap.append(color.color.values[0])

                selectedPartitions.append(part)

        if cmap and len(cmap) < 2:
            cmap.append(cmap[0])

        if not selectedPartitions:
            cmap = None

        return cmap, selectedPartitions