import pandas as pd
import streamlit as st

class ModelParameter:
    def __init__(self, tabMenu):
        self.globals = st.session_state.GLOBALS

        st.markdown("""
    <style>
    [data-testid=column]:nth-of-type(1) [data-testid=stVerticalBlock]{
        gap: 0rem;
    }
    </style>
    """,unsafe_allow_html=True)

        modelTypeRow = st.columns([3,3,1], gap="small", vertical_alignment="center")
        modelTypeRow[0].markdown(self.globals.EditParameter['modelType'])
        modelTypeRow[1].markdown(
            str('3D' if st.session_state.configuration['model']['3d'] else '2.5D')
        )
        modelTypeRow[2].button(":pencil2:",
            on_click=st.session_state.handler.btnApiWizardRun,
            args=['modelType'],
            key='modelType',
        )

        st.divider()
        setModelParameterCP1Row = st.columns(
            [3,3,1], gap="small", vertical_alignment="center"
        )
        setModelParameterCP1Row[0].markdown(self.globals.EditParameter['cornerPoint1'])
        setModelParameterCP1Row[1].markdown(", ".join(
            str(
                value
            ) for value in st.session_state.configuration['model']['cornerPoint1']
        ))

        setModelParameterCP2Row = \
            st.columns([3,3,1], gap="small", vertical_alignment="center")
        setModelParameterCP2Row[0].markdown(self.globals.EditParameter['cornerPoint2'])
        setModelParameterCP2Row[1].markdown(", ".join(
            str(
                value
            ) for value in st.session_state.configuration['model']['cornerPoint2']
        ))

        setModelParameterDimRow = st.columns(
            [3,3,1],
            gap="small",
            vertical_alignment="center"
        )
        setModelParameterDimRow[0].markdown(self.globals.EditParameter['dimension'])
        setModelParameterDimRow[1].markdown(", ".join(
            str(value) for value in st.session_state.configuration['model']['dimension']
        ))
        setModelParameterDimRow[2].button(
            ":pencil2:",
            on_click=st.session_state.handler.btnApiWizardRun,
            args=['setModelParameter'],
            key='setModelParameterDim',
        )


        if st.session_state.configuration['model']['discretisationType'] == 'd':
            discretisationType = \
                self.globals.wizard['SetDiscretisation']['typeTextDiscret']
        else:
            discretisationType = \
                self.globals.wizard['SetDiscretisation']['typeTextConstant']

        if st.session_state.configuration['model']['discretisationType'] == 'd':

            st.divider()
            setModelParameterDimRow = st.columns(
                [3,3,1],
                gap="small",
                vertical_alignment="center"
            )
            setModelParameterDimRow[0].markdown(self.globals.EditParameter['discretisationType'] + discretisationType)

            setModelParameterDimRow[2].button(
                ":pencil2:",
                on_click=st.session_state.handler.btnApiWizardRun,
                args=['setDiscretisation'],
                key='setDiscretisation',
            )

            dx = [1,1,1]
            dy = [1,1,1]
            dz = [1,1,1]

            if 'discretisationX' in st.session_state.configuration['model']:
                    dx = st.session_state.configuration['model']['discretisationX']

            if 'discretisationY' in st.session_state.configuration['model']:
                    dy = st.session_state.configuration['model']['discretisationY']

            if 'discretisationZ' in st.session_state.configuration['model']:
                    dz = st.session_state.configuration['model']['discretisationZ']

            discretisationDiscret = pd.DataFrame.from_dict(
                dict(
                    dx=dx,
                    dy=dy,
                    dz=dz
                ),
                orient='index'
            ).transpose()

            st.dataframe(discretisationDiscret, hide_index=True)
        else:
            st.divider()
            setModelParameterDimRow = st.columns(
                [3,3,1],
                gap="small",
                vertical_alignment="center"
            )
            setModelParameterDimRow[0].markdown(self.globals.EditParameter['discretisationConstant'])
            valuesAsString = str(st.session_state.configuration['model']['cellNumberX'])+\
                ", " + str(st.session_state.configuration['model']['cellNumberY']) + ", "\
                + str(st.session_state.configuration['model']['cellNumberZ'])
            setModelParameterDimRow[1].markdown(valuesAsString)
            setModelParameterDimRow[2].button(
                ":pencil2:",
                on_click=st.session_state.handler.btnApiWizardRun,
                args=['setDiscretisation'],
                key='setDiscretisation',
            )


        st.divider()

        structureName = 'layer'
        self.listOfStructureFiles(structureName)

        structureName = 'fault'
        self.listOfStructureFiles(structureName)

        structureName = 'mask'
        self.listOfStructureFiles(structureName)

        self.createTableOfStructureDimensionData('fault', 'seams', 'Width')
        self.createTableOfStructureDimensionData('layer', 'fault', 'Rank')


    def listOfStructureFiles(self, structureType) -> None:

        listOfStructures = st.columns([6,1], gap="small", vertical_alignment="center")
        if 'structure' in st.session_state.configuration:

            if st.session_state.configuration['structure']['file'] and \
                structureType in st.session_state.configuration['structure']['type']:

                structureSurfaceList = []
                for i in st.session_state.configuration['gui']['surfaceColor']['surface']:
                    structureSurfaceList.append(i)

                structureFileList = []
                for i, file in enumerate(
                    st.session_state.configuration['structure']['file']
                ):
                    structureFileList.append(file.split(".")[0])

                pnames = []
                pids = []
                pcolor = []

                for part in st.session_state.configuration['structure']['file']:
                    partitionName = part.split(".")[0]
                    index = structureFileList.index(partitionName)

                    if st.session_state.configuration['structure']['type'][index] == \
                        structureType:
                        pnames.append(
                            st.session_state.configuration['structure']['file'][index]
                        )
                        id = structureSurfaceList.index(partitionName)
                        pids.append(id)
                        pcolor.append(
                            st.session_state.configuration['gui'][
                                'surfaceColor'
                            ]['color'][id]
                        )


                structure = dict(Name=pnames, Id=pids, Color=pcolor)
                df = pd.DataFrame.from_dict(structure, orient='index').transpose()
                df.rename(columns={'name' : structureType + ' filename'}, inplace = True)
                if pnames:

                    df = df.style.apply(self.colorize, axis=1)
                    listOfStructures[0].dataframe(
                        df,
                        column_config={
                            "name": st.column_config.Column(disabled=True),
                            "Color" : None
                        },
                        hide_index=True,
                    )
                else:
                    listOfStructures[0].markdown("No " + structureType + " files")
            else:
                listOfStructures[0].markdown("No " + structureType + " files")


            listOfStructures[1].button(
                ":pencil2:",
                on_click=st.session_state.handler.btnApiWizardRun,
                args=['load' + structureType.capitalize()  + "s"],
                key=structureType,
            )


    def createTableOfStructureDimensionData(
        self,
        structureType1 = 'layer',
        structureType2 = 'fault',
        typeName = 'Rank'
    ) -> None:
        listOfStructures = st.columns([6,1], gap="small", vertical_alignment="center")
        pnames = []
        pvalues = []
        pcolors = []


        structurePartitionList = []
        for i in st.session_state.configuration['gui']['partitionColor']['partition']:
            structurePartitionList.append(i)

        structureFileList = []
        for i, file in enumerate(st.session_state.configuration['structure']['file']):
            structureFileList.append(file.split(".")[0])

        for part in st.session_state.configuration['model']['structure'+typeName].keys():

            index = structureFileList.index(part)
            if st.session_state.configuration['structure']['type'][index] == \
                structureType1 or \
                st.session_state.configuration['structure']['type'][index] == \
                structureType2:
                pnames.append(part)
                pvalues.append(
                    st.session_state.configuration['model']['structure' + typeName][part]
                )

                index = structurePartitionList.index(part)
                pcolors.append(
                     st.session_state.configuration['gui'][
                        'partitionColor'
                    ]['color'][index]
                )

        structure = dict(Name=pnames, Rank=pvalues, Color=pcolors)
        df = pd.DataFrame.from_dict(structure, orient='index').transpose()
        if typeName.lower() == "width":
            df.rename(columns={'Rank' : typeName.capitalize() + ' (m)'}, inplace = True)
        else:
            df.rename(columns={'Rank' : typeName.capitalize()}, inplace = True)

        if pnames:

            df = df.style.apply(self.colorize, axis=1)

            listOfStructures[0].dataframe(
                df,
                column_config={
                    "Name": st.column_config.Column(disabled=True),
                    "Color": None,
                },
                hide_index=True
            )
        else:
            listOfStructures[0].markdown(
                "No structures (layer, faults) loaded for " + typeName.lower() + ""
            )

        listOfStructures[1].button(
            ":pencil2:",
            on_click=st.session_state.handler.btnApiWizardRun,
            args=['setStructure' + typeName],
            key=typeName,
        )


    def colorize(self, color):
        return [
            f'background-color: {color.Color}'
        ]*len(color) if color.Color[0] == '#' else ['background-color: white']*len(color)