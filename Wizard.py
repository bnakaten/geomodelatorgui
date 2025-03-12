import streamlit as st
import pandas as pd

from PIL import Image


class Wizard():
    globals = ''
    numberOfSteps = 8

    def __init__(self):
        self.globals = st.session_state.GLOBALS

    def step0(self):
        (DemoOrCustom()).run()

    def step1(self):
        (TypeOfModel()).run()

    def step2(self):
        (LoadLayers()).run()

    def step3(self):
        (LoadOtherStructures()).run()

    def step4(self):
        (LoadMask()).run()

    def step5(self):
        (SetModelParameter()).run()

    def step6(self):
        (SetDiscretisation()).run()

    def step7(self):
        (SetStructureWidth()).run()

    def step8(self):
        (SetStructureRank()).run()

    def setStep(self, action, step=None):
        if action == self.globals.wizard['nextButton']:
            st.session_state.previousLayerFiles = False
            st.session_state.previousFaultFiles = False
            st.session_state.wizardSteps = st.session_state.wizardSteps + 1
        if action == self.globals.wizard['backButton']:
            st.session_state.wizardSteps = st.session_state.wizardSteps - 1
        if action == self.globals.wizard['startButton']:
            st.session_state.wizardSteps = 0

    @st.dialog('Model configuration', width="large")
    def windowNavigation(self):
        globals = st.session_state.GLOBALS

        st.divider()
        if st.session_state.btnApiGmlRun:
            st.rerun()

        steps = Wizard()

        for i in range(0, self.numberOfSteps+1):
            if st.session_state.wizardSteps == i:
                stepMethodName = 'step' + str(i)
                runMethod = getattr(steps, stepMethodName)
                runMethod()

        disableBackButton = True if st.session_state.wizardSteps == 0 else False

        st.divider()
        formFooterCols = st.columns([3,2,2,2,2], gap="small", vertical_alignment="bottom")

        logo = Image.open(st.session_state.GLOBALS.default['logo'])
        formFooterCols[0].image(logo, width=150)

        resetBtn = False

        if st.session_state.wizardSteps == 0:
            formFooterCols[2].button(
                globals.wizard['demoButton'], on_click=self.btnDemoRun
            )
            formFooterCols[3].button(
                globals.wizard['customButton'], on_click=steps.setStep, args=['Next']
            )
        elif st.session_state.wizardSteps < self.numberOfSteps:
            # resetBtn = formFooterCols[1].button(
            #     globals.wizard['resetButton'],
            #     on_click=self.btnReset
            # )
            formFooterCols[2].button(
                globals.wizard['backButton'],
                on_click=steps.setStep,
                args=['Back'],
                disabled=disableBackButton
            )
            formFooterCols[3].button(
                globals.wizard['nextButton'],
                on_click=steps.setStep,
                args=['Next']
            )
            formFooterCols[4].button(
                globals.wizard['runButton'],
                on_click=st.session_state.handler.btnApiGmlRun,
                type="primary"
            )
        else:
            # resetBtn = formFooterCols[1].button(
            #     globals.wizard['resetButton'],
            #     on_click=self.btnReset
            # )
            formFooterCols[2].button(
                globals.wizard['backButton'],
                on_click=steps.setStep,
                args=['Back'],
                disabled=disableBackButton
            )
            formFooterCols[3].button(
                globals.wizard['runButton'],
                on_click=st.session_state.handler.btnApiGmlRun,
                type="primary"
            )

        if resetBtn:
            st.rerun()


    def btnReset(self) -> None:
        st.session_state.stateApiGmlConfigure = False
        st.session_state.wizardSteps = 0
        st.session_state.handler.cleanDirectory(
            st.session_state.GLOBALS.default['uploadPath']
        )
        st.session_state.handler.tearDown()

    def btnDemoRun(self) -> None:
        st.session_state.useDemoModel = True
        st.session_state.handler.loadDemoModel()
        st.session_state.btnApiGmlRun = True
        st.session_state.wizardWindow = False


class WizardPage:
    def __init__(self):
        self.globals = st.session_state.GLOBALS.wizard[self.__class__.__name__]

        self.c1, self.c2 = st.columns(2)
        self.c1.header(self.globals['header'])
        self.c1.image(self.globals['image'])


    def btnConfigSave(self):
        st.session_state.stateApiGmlConfigure = False
        st.session_state.handler.writeConfigurationFromSessionStateIntoFile(
            st.session_state.configuration
        )
        st.session_state.gmlConfigurationChange = True

class WizardPageWithDescitption(WizardPage):
    def __init__(self):
        self.globals = st.session_state.GLOBALS.wizard[self.__class__.__name__]

        self.c1, self.c2 = st.columns(2)
        self.c1.header(self.globals['header'])
        self.c1.text(self.globals['descriptionText'], help=self.globals['descriptionHelper'])
        self.c1.image(self.globals['image'])


    def btnLoadFiles(self, structureName='layer') -> None:
        ext = tuple(st.session_state.GLOBALS.info['pointCloudFileExtensions'])
        for uploadedFile in st.session_state[
            'uploaded' + structureName.capitalize() + 'Files'
        ]:
            if uploadedFile.name.endswith(ext):
                if uploadedFile.name.endswith(ext):
                    st.session_state.handler.createStructureFile(
                        uploadedFile,
                        structureName
                    )
                else: False

        st.session_state.handler.writeConfigurationFromSessionStateIntoFile(
            st.session_state.configuration
        )


    def removeFiles(self, structureName='layer') -> None:
        uploadedFiles = [
            file.name for file in st.session_state[
                'uploaded' + structureName.capitalize() + 'Files'
            ]
        ] if st.session_state.uploadedLayerFiles else []

        for item in st.session_state['previous' + structureName.capitalize() + 'Files']:
            if item not in uploadedFiles:
                i = st.session_state.configuration['structure']['file'].index(item)
                st.session_state.configuration['structure']['file'].pop(i)
                st.session_state.configuration['structure']['extension'].pop(i)
                st.session_state.configuration['structure']['type'].pop(i)

        st.session_state.handler.writeConfigurationFromSessionStateIntoFile(
            st.session_state.configuration
        )


    def btnDeleteFiles(self, structureName='layer') -> None:
        if structureName == 'layer' or structureName == 'fault':
            for item in st.session_state['delete' + structureName.capitalize()]:
                i = st.session_state.configuration['structure']['file'].index(item)
                st.session_state.configuration['structure']['file'].pop(i)
                st.session_state.configuration['structure']['extension'].pop(i)
                st.session_state.configuration['structure']['type'].pop(i)


                st.session_state.configuration['model']['structureRank'].pop(
                    item.split('.')[0]
                )
                if structureName == 'fault':
                    st.session_state.configuration['model']['structureWidth'].pop(
                        item.split('.')[0]
                    )

            for item in st.session_state.configuration['structure']['type']:
                if item == 'mask':
                    i = st.session_state.configuration['structure']['type'].index(item)
                    st.session_state.configuration['structure']['file'].pop(i)
                    st.session_state.configuration['structure']['extension'].pop(i)
                    st.session_state.configuration['structure']['type'].pop(i)

        st.session_state.handler.writeConfigurationFromSessionStateIntoFile(
            st.session_state.configuration
        )


    def loadPreviousFiles(self, structureName='layer') -> None:

        fileExtensions = st.session_state.GLOBALS.info['pointCloudFileExtensions']

        key = 'uploaded' + structureName.capitalize() + 'Files'
        # a = st.session_state[key]
        uploadedFiles = self.c2.file_uploader(
            self.globals['fileUploaderText'],
            accept_multiple_files=True,
            type=fileExtensions,
            key=key
        )

        if uploadedFiles:
            if isinstance(
                st.session_state['previous' +structureName.capitalize() + 'Files'], bool
            ):
                st.session_state['previous' + structureName.capitalize() + 'Files'] = []
            currentFiles = \
                [file.name for file in uploadedFiles] if uploadedFiles else []

            removedFiles = \
                list(
                    set(
                        st.session_state['previous'+structureName.capitalize()+'Files']
                    ) - set(currentFiles)
                )

            if not removedFiles:
                self.btnLoadFiles(structureName)
            else:
                self.removeFiles(structureName)

            st.session_state['previous' +structureName.capitalize() + 'Files'] = \
                currentFiles

        elif not uploadedFiles and \
            st.session_state['previous' + structureName.capitalize() + 'Files']:
            st.session_state['previous' + structureName.capitalize() + 'Files'] = \
                uploadedFiles
            self.removeFiles(structureName)
            st.session_state['previous' + structureName.capitalize() + 'Files'] = []

        if 'structure' in st.session_state.configuration:

            if st.session_state.configuration['structure']['file'] and \
                structureName in st.session_state.configuration['structure']['type']:
                formDelete = self.c2.form('DeleteStructure')


                tmpFiles = []

                for i, item in enumerate(
                    st.session_state.configuration['structure']['type']
                ):
                    if item == structureName:
                        tmpFiles.append(
                            st.session_state.configuration['structure']['file'][i]
                        )

                formDelete.multiselect(
                    self.globals['previousUploadedFilesText'],
                    tmpFiles,
                    key='delete' + structureName.capitalize()
                )

                formDelete.form_submit_button(
                    self.globals['deleteFileButton'],
                    on_click=self.btnDeleteFiles,
                    args=[structureName]
                )

class DemoOrCustom(WizardPage):
    def run(self):
        if 'step0' not in st.session_state:
            st.session_state.handler.cleanDirectory(
                st.session_state.GLOBALS.default['uploadPath']
            )
            st.session_state.handler.createDummyConfigurationFile()
            st.session_state.useDemoModel = True
            st.session_state.handler.loadConfiguration('dummy')
            st.session_state.step0 = True

class TypeOfModel(WizardPage):
    def run(self):
        radioBoxIndex =  1 if st.session_state.configuration['model']['3d'] else 0
        self.c2.radio(
            self.globals['radioButton']['text'],
            [
                self.globals['radioButton']['option1Text'],
                self.globals['radioButton']['option2Text']
            ],
            captions = [
                self.globals['radioButton']['caption1'],
                self.globals['radioButton']['caption2']
            ],
            index=radioBoxIndex,
            on_change=self.changeModelType,
            key="formModelType",
            horizontal=False)


    def changeModelType(self):
        st.session_state.configuration['model']['3d'] = \
            True if st.session_state.formModelType == '**3d**' else False
        self.btnConfigSave()


class LoadLayers(WizardPageWithDescitption):
    def run(self):
        self.loadPreviousFiles()


class LoadOtherStructures(WizardPageWithDescitption):
    def run(self):
        self.loadPreviousFiles('fault')


class LoadMask(WizardPageWithDescitption):
    def run(self):
        fileExtensions = st.session_state.GLOBALS.info['pointCloudFileExtensions'] + \
            st.session_state.GLOBALS.info['shapeFileExtensions']

        uploadedFiles = self.c2.file_uploader(
            self.globals['fileUploaderText'],
            accept_multiple_files=True,
            type=fileExtensions,
            key="uploadedMaskFiles",
        )

        if uploadedFiles:
            if 'structure' in st.session_state.configuration:
                self.btnDeleteFiles('mask')
            self.btnReplaceFile()

        if not uploadedFiles and 'structure' in st.session_state.configuration:

            if st.session_state.configuration['structure']['file'] and \
                'mask' in st.session_state.configuration['structure']['type']:
                formDeleteMask = self.c2.form('formDeleteMask')
                tmpFaultFiles = []

                for i, item in enumerate(
                    st.session_state.configuration['structure']['type']
                ):
                    if item == 'mask':
                        tmpFaultFiles.append(
                            st.session_state.configuration['structure']['file'][i]
                        )

                formDeleteMask.multiselect(
                    self.globals['previousUploadedFilesText'],
                    tmpFaultFiles,
                    key='deleteMask'
                )

                formDeleteMask.form_submit_button(
                    self.globals['deleteFileButton'],
                    on_click=self.btnReplaceFile,
                )


    def btnReplaceFile(self):
        ext = tuple(st.session_state.GLOBALS.info['pointCloudFileExtensions'])
        uploadedFile = st.session_state.uploadedMaskFiles

        for uploadedFile in st.session_state['uploadedMaskFiles']:
            if uploadedFile.name.endswith(ext):
                st.session_state.handler.createStructureFile(
                    uploadedFile, 'mask'
                ) if uploadedFile.name.endswith(ext) else False

            st.session_state.handler.writeConfigurationFromSessionStateIntoFile(
                st.session_state.configuration
            )


class SetModelParameter(WizardPageWithDescitption):
    def run(self):
        formMainDetails = self.c2.form('formMainDetails')

        try:
            cornerPoint1 = ",".join(map(
                str, st.session_state.configuration['model']['cornerPoint1']
            )) if 'cornerPoint1' in st.session_state.configuration['model'] else "0,0,0"
            cornerPoint1 = formMainDetails.text_input(
                self.globals['cornerPoint1Text'], value=cornerPoint1, key='cornerPoint1'
            )
            cornerPoint2 = ",".join(map(
                str, st.session_state.configuration['model']['cornerPoint2']
            )) if 'cornerPoint2' in st.session_state.configuration['model'] else "5,0,0"
            cornerPoint2 = formMainDetails.text_input(
                self.globals['cornerPoint2Text'], value=cornerPoint2, key='cornerPoint2',
                help=self.globals['modelDimensionInfo']
            )

            if len(cornerPoint1.split(',')) != 3:
                raise OverflowError
            if cornerPoint1.split(',').count(""):
                raise ValueError

            if len(cornerPoint2.split(',')) != 3:
                raise OverflowError
            if cornerPoint2.split(',').count(""):
                raise ValueError

            formMainDetails.markdown(self.globals['modelDimension'])
            c1, c2, c3 = formMainDetails.columns(3)

            if 'dimension' in st.session_state.configuration['model']:
                dimension = st.session_state.configuration['model']['dimension']
            else:
                dimension = "6,10,7"

            c1.number_input(
                self.globals['modelDimensionXText'],
                min_value=1.0,
                step=1.0,
                key='xDimension',
                value=float(dimension[0])
            )

            c2.number_input(
                self.globals['modelDimensionYText'],
                min_value=1.0,
                step=1.0,
                key='yDimension',
                value=float(dimension[1])
            )

            c3.number_input(
                self.globals['modelDimensionZText'],
                min_value=1.0,
                step=1.0,
                key='zDimension',
                value=float(dimension[2])
            )
        except ValueError:
            formMainDetails.error(self.globals['modelDimensionValueError'])
        except OverflowError:
            formMainDetails.error(self.globals['modelDimensionOverflowError'])

        formMainDetails.form_submit_button(
            self.globals['saveButton'],
            on_click=self.changewizardState,
            type='primary',
        )

    def changewizardState(self):
        st.session_state.configuration['model']['cornerPoint1'] = \
            [float(x) for x in st.session_state.cornerPoint1.split(',')]
        st.session_state.configuration['model']['cornerPoint2'] = \
            [float(x) for x in st.session_state.cornerPoint2.split(',')]
        st.session_state.configuration['model']['dimension'] = \
            [
                st.session_state.xDimension,
                st.session_state.yDimension,
                st.session_state.zDimension
            ]

        self.btnConfigSave()


class SetDiscretisation(WizardPage):
    def run(self):
        discretisation = st.session_state.configuration['model']['discretisationType']

        st.session_state.discretisationType = self.c2.toggle(
            self.globals['toggleButton'],
            value = (True if discretisation == 'n' else False),
            on_change=self.tglDiscretisation,
        )

        formMinorDetails = self.c2.form('saveMinorDetails')

        if st.session_state.discretisationType:

            discretisationContinous  = formMinorDetails.text_input(
            self.globals['textInputConstant'],
                st.session_state.discretisationContinous
            )
        else:
            discretisationDiscret = formMinorDetails.data_editor(
                st.session_state.discretisationDiscret,
                column_config={
                    "dx": st.column_config.NumberColumn(
                        help=self.globals['textInputDiscret'],
                    ),
                    "dy": st.column_config.NumberColumn(
                        help=self.globals['textInputDiscret'],
                    ),
                    "dz": st.column_config.NumberColumn(
                        help=self.globals['textInputDiscret'],
                    )
                    },
                num_rows='dynamic'
            )

            formMinorDetails.text('', help=self.globals['textInputDiscret'])

        btnMinorDetails = formMinorDetails.form_submit_button(
            self.globals['saveButton'],
            type='primary',
        )

        if btnMinorDetails:

            if st.session_state.discretisationType:
                try:
                    discretisationContinous = discretisationContinous.split(',')
                    if len(discretisationContinous) != 3:
                        raise OverflowError

                    st.session_state.configuration['model']['cellNumberX'] = \
                        int(discretisationContinous[0])
                    st.session_state.configuration['model']['cellNumberY'] = \
                        int(discretisationContinous[1])
                    st.session_state.configuration['model']['cellNumberZ'] = \
                        int(discretisationContinous[2])
                except ValueError:
                    formMinorDetails.error(self.globals['modelDiscretisationValueError'])
                except OverflowError:
                    formMinorDetails.error(self.globals['modelDiscretisationOverflowError'])
            else:
                if discretisationDiscret['dx'].sum() > \
                    st.session_state.configuration['model']['dimension'][0]:
                    self.c2.error(self.globals['textInputDiscret'])
                else:
                    st.session_state.configuration['model']['discretisationX'] = \
                        list(discretisationDiscret['dx'])

                if discretisationDiscret['dy'].sum() > \
                    st.session_state.configuration['model']['dimension'][1]:
                    self.c2.error(self.globals['textInputDiscret'])
                else:
                    st.session_state.configuration['model']['discretisationY'] = \
                        list(discretisationDiscret['dy'])

                if discretisationDiscret['dz'].sum() > \
                    st.session_state.configuration['model']['dimension'][2]:
                    self.c2.error(self.globals['textInputDiscret'])
                else:
                    st.session_state.configuration['model']['discretisationZ'] = \
                        list(discretisationDiscret['dz'])

            self.btnConfigSave()


    def tglDiscretisation(self):
        if st.session_state.discretisationType and \
            st.session_state.configuration['model']['discretisationType'] == 'n':
            st.session_state.configuration['model']['discretisationType'] = 'd'
        elif st.session_state.discretisationType == False and \
            st.session_state.configuration['model']['discretisationType'] == 'd':
            st.session_state.configuration['model']['discretisationType'] = 'n'


class SetStructureWidth(WizardPage):
    def run(self):
        formSubDetailsA = self.c2.form('saveSubDetailsA')

        pnames = []
        pvalues = []

        structureList = []
        for i, file in enumerate(st.session_state.configuration['structure']['file']):
            structureList.append(file.split(".")[0])

        for structureName, structureValue \
            in st.session_state.configuration['model']['structureWidth'].items():
            try:
                index = structureList.index(structureName)
                if st.session_state.configuration['structure']['type'][index] == 'fault':
                    pnames.append(structureName)
                    pvalues.append(structureValue)
            except ValueError:
                pass

        structureWidth = dict(Name=pnames, Width=pvalues)
        st.session_state.structureWidth = \
            pd.DataFrame.from_dict(structureWidth, orient='index').transpose()
        st.session_state.structureWidth['Width'] = \
            st.session_state.structureWidth['Width'].astype(float)


        st.session_state.structureWidth.rename(columns={'Width' : 'Width (m)'}, inplace = True)

        st.session_state.structureWidthE = formSubDetailsA.data_editor(
            st.session_state.structureWidth,
            column_config={
                "Name": st.column_config.Column(disabled=True),
                "color": None,
            },
            hide_index = True,
            num_rows = 'fixed',
        )

        btnSubDetailsA = formSubDetailsA.form_submit_button(
            self.globals['saveButton'],
            type='primary',
        )

        if btnSubDetailsA:
            st.session_state.configuration['model']['structureWidth'] = dict(
                zip(
                    st.session_state.structureWidthE['Name'],
                    st.session_state.structureWidthE['Width']
                )
            )
            self.btnConfigSave()


class SetStructureRank(WizardPage):
    def run(self):
        formSubDetailsA = self.c2.form('saveSubDetailsA')

        pnames = []
        pvalues = []

        structureList = []
        for i, file in enumerate(st.session_state.configuration['structure']['file']):
            structureList.append(file.split(".")[0])

        for structureName, structureValue \
            in st.session_state.configuration['model']['structureRank'].items():
            try:
                index = structureList.index(structureName)
                if st.session_state.configuration['structure']['type'][index] == 'layer' \
                    or \
                    st.session_state.configuration['structure']['type'][index] == 'fault':
                    pnames.append(structureName)
                    pvalues.append(structureValue)
            except ValueError:
                pass

        structureRank = dict(Name=pnames, Rank=pvalues)
        st.session_state.structureRank = \
            pd.DataFrame.from_dict(structureRank, orient='index').transpose()
        st.session_state.structureRank['Rank'] = \
            st.session_state.structureRank['Rank'].astype(int)

        st.session_state.structureRankE = formSubDetailsA.data_editor(
            st.session_state.structureRank,
            column_config={
                "Name": st.column_config.Column(disabled=True),
                "color": None,
            },
            hide_index = True,
            num_rows = 'fixed',
        )


        formSubDetailsA.text("", help=self.globals['textInfo'])

        btnSubDetailsA = formSubDetailsA.form_submit_button(
            self.globals['saveButton'],
            type='primary',
        )

        if btnSubDetailsA:
            st.session_state.configuration['model']['structureRank'] = dict(
                zip(
                    st.session_state.structureRankE.Name,
                    st.session_state.structureRankE.Rank
                )
            )
            self.btnConfigSave()