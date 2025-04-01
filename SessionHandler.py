# SPDX-FileCopyrightText: 2025 Benjamin Nakaten (GFZ) <bnakaten@gfz-potsdam.de>
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
#
# SPDX-License-Identifier: GPL-3.0-only

import glob
import json
import yaml
import os
import sys
import pandas as pd
import requests
import streamlit as st
import shutil


class SessionHandler:
    globals = []

    def __init__(
        self,
        apiSession=requests.session(),
        globals=''
     ) -> None:

        self.globals = globals
        st.session_state.GLOBALS = globals

        if 'wizardWindow' not in st.session_state:
            st.session_state.wizardWindow = True

        if 'wizardSteps' not in st.session_state:
            st.session_state.wizardSteps = 0

        if 'uploadedLayerFiles' not in st.session_state:
            st.session_state.uploadedLayerFiles = []

        if 'previousLayerFiles' not in st.session_state:
            st.session_state.previousLayerFiles = []

        if 'uploadedFaultFiles' not in st.session_state:
            st.session_state.uploadedFaultFiles = []

        if 'previousFaultFiles' not in st.session_state:
            st.session_state.previousFaultFiles = []

        if 'plottercolor' not in st.session_state:
            st.session_state.plottercolor = globals.default['stpyvistaBackgroundColor']

        if 'configuration' not in st.session_state:
            st.session_state.configuration = False

        if 'plot' not in st.session_state:
            st.session_state.plot = False

        if 'stateApiGmlConfigure' not in st.session_state:
            st.session_state.stateApiGmlConfigure = False

        if 'stateApiGmlRun' not in st.session_state:
            st.session_state.stateApiGmlRun = False

        if 'useDemoModel' not in st.session_state:
            st.session_stateuseDemoModel = True
            self.loadDemoModel()

        if "configuration" not in st.session_state:
            self.loadConfiguration()

        if "apiSession" not in st.session_state:
            st.session_state.apiSession = apiSession

        if "fileUploader" not in st.session_state:
            st.session_state.fileUploader = False

        if "btnApiGmlConfigure" not in st.session_state:
            st.session_state.btnApiGmlConfigure = False

        if "btnApiGmlRun" not in st.session_state:
            st.session_state.btnApiGmlRun = False

        if "tabs" not in st.session_state:
            st.session_state.tabs = []
            for tab, tabLable in globals.viewTab.items():
                st.session_state.tabs.append(tabLable)

        if "model" not in st.session_state.configuration:
            st.session_state.configuration['model'] = {}


        if 'model' in st.session_state.configuration:

            if 'structure' not in st.session_state.configuration:
                st.session_state.configuration['structure'] = {}
                st.session_state.configuration['structure']['file'] = []

                try:
                    for file in st.session_state.configuration['structure']['file']:
                        if file.split('.')[0] not in \
                            st.session_state.configuration['model']['structureWidth']:
                            st.session_state.configuration[
                                'model'
                            ]['structureWidth'][file.split('.')[0]] = 10

                        if file.split('.')[0] not in \
                            st.session_state.configuration['model']['structureRank']:
                            st.session_state.configuration[
                                'model'
                            ]['structureRank'][file.split('.')[0]] = 0
                except:
                    st.session_state.configuration['structure']['file'] = []


        if "structureWidth" not in st.session_state.configuration["model"]:
            st.session_state.configuration['model']['structureWidth'] = {}

        if "structureRank" not in st.session_state.configuration["model"]:
            st.session_state.configuration['model']['structureRank'] = {}

        self.setLayerSurfaceColors()

        self.discretisationFormHandle()


    def setLayerSurfaceColors(self):
        pnames = []
        pvalues = []
        pcolors = []

        if st.session_state.configuration['model']['structureWidth']:

            for part in st.session_state.configuration['model']['structureWidth'].keys():
                if 'fault' in part or 'seam' in part:
                    pnames.append(part)
                    pvalues.append(
                        st.session_state.configuration['model']['structureWidth'][part]
                    )
                    pcolors.append('#ffffff')


            structureWidth = dict(Name=pnames, Width=pvalues, color=pcolors)
            st.session_state.structureWidth = \
                pd.DataFrame.from_dict(structureWidth, orient='index').transpose()
            st.session_state.structureWidth['"Width'] = \
                st.session_state.structureWidth['Width'].astype(float)
        else:
            st.session_state.configuration['model']['structureWidth'] = {}

        pnames = []
        pvalues = []
        pcolors = []

        if st.session_state.configuration['model']['structureRank']:
            for part in st.session_state.configuration['model']['structureRank'].keys():
                if 'layer' in part or 'fault' in part:
                    pnames.append(part)
                    pvalues.append(
                        st.session_state.configuration['model']['structureRank'][part]
                    )
                    pcolors.append('#ffffff')

            structureRank = dict(Name=pnames, Rank=pvalues, color=pcolors)
            st.session_state.structureRank = \
                pd.DataFrame.from_dict(structureRank, orient='index').transpose()
            st.session_state.structureRank['Rank'] = \
                st.session_state.structureRank['Rank'].astype(int)

        else:
            st.session_state.configuration['model']['structureRank'] = {}



    def loadConfiguration(self, sourceType='demo'):
        configurationFilesFilename = self.globals.default['uploadPath'] + \
            self.globals.default['configurationFileName'] + '.json'

        try:
            configurationFiles, extension = self.getConfigurationFile(sourceType)
            configurationFilesFilename = \
                self.globals.default['uploadPath'] + configurationFiles

            jsonFilename = \
                self.globals.default['uploadPath'] + \
                self.globals.default['configurationFileName'] + '.json'

            if extension == 'yaml':
                with open(configurationFilesFilename, 'r') as fileHandle:
                    configuration = yaml.safe_load(fileHandle)

                with open(jsonFilename, 'w+') as fileHandle:
                    json.dump(configuration, fileHandle)

            with open(jsonFilename, 'r') as fileHandle:
                st.session_state.configuration = json.load(fileHandle)
                st.session_state.configuration['config']['file'] = \
                    os.path.basename(fileHandle.name)
        except:
            st.exception(RuntimeError(
                'Unvalid configuration file ' + configurationFilesFilename + \
                '. Configuration file format not readable.'
            ))


    @staticmethod
    def ensureDirectoryExists(directoryPath):
        if not os.path.exists(directoryPath):
            os.makedirs(directoryPath)


    def loadDemoModel(self):
        st.session_state.stateApiGmlConfigure = False

        self.ensureDirectoryExists(self.globals.default['uploadPath'])
        self.cleanDirectory(self.globals.default['uploadPath'])

        onlyFilesWithExtension = self.globals.info['configurationFileExtensions'] + \
            self.globals.info['pointCloudFileExtensions']
        self.cloneDirectoryContentToDestination(
            self.globals.default['defaultPath'],
            self.globals.default['uploadPath'],
            onlyFilesWithExtension
        )

        self.loadConfiguration()

        st.session_state.configuration['config']['base'] = \
            self.globals.default['uploadPath']

        st.session_state.configuration['config']['inputPath'] = ''
        st.session_state.configuration['config']['outputPath'] = ''
        st.session_state.configuration['config']['shapePath'] = ''
        st.session_state.configuration['config']['modelFileVtk'] = \
            self.globals.default['modelFileVtk']

        st.session_state.configuration['config']['csv']['compress'] = True

        self.writeConfigurationFromSessionStateIntoFile(st.session_state.configuration)


    def getConfigurationFile(self, sourceType='demo'):
        configurationFile = ''
        configurationFileExtension = 'json'

        noConfigurationFile = True
        ext = tuple(self.globals.info['configurationFileExtensions'])
        if sourceType == 'upload':
            for uploadedFile in st.session_state.fileuploader:
                if uploadedFile.name.endswith(ext):
                    configurationFile = uploadedFile.name
                    self.createConfigFile(uploadedFile)
                    configurationFileExtension = uploadedFile.name.split('.')[-1]
                    noConfigurationFile = False
                    break

            if noConfigurationFile:
                configurationFile = self.createDummyConfigurationFile()

        elif sourceType == 'dummy':
            configurationFile = self.createDummyConfigurationFile()
        else:
            path = self.globals.default['uploadPath']

            for file in os.listdir(path):
                if file.endswith(ext):
                    configurationFile = file
                    configurationFileExtension = configurationFile.split('.')[-1]
                    break

        return configurationFile, configurationFileExtension


    def createConfigFile(self, file):
        byteData = file.read()

        st.session_state.configuration['config']['base'] = \
            self.globals.default['uploadPath']
        file = self.globals.default['uploadPath']  + file.name
        with open(file, "wb+") as fileHandle:
            fileHandle.write(byteData)

    def createDummyConfigurationFile(self):
        configuration = {}
        configuration['config'] = {}
        configuration['config']['file'] = \
            self.globals.default['configurationFileName'] + '.json'
        configuration['config']['base'] = self.globals.default['uploadPath']
        configuration['config']['inputPath'] = ''
        configuration['config']['outputPath'] = ''
        configuration['config']['sourcePath'] = ''
        configuration['config']['modelFileVtk'] = self.globals.default['modelFileVtk']
        configuration['config']['csv'] = {}
        configuration['config']['csv']['columns'] = ['x', 'y', 'z']
        configuration['config']['csv']['delimiter'] = ','
        configuration['config']['csv']['header'] = 1
        configuration['config']['csv']['compress'] = True

        configuration['model'] = {}
        configuration['model']['3d'] = True
        configuration['model']['dimension'] = [1, 1, 1]
        configuration['model']['discretisationType'] = 'n'
        configuration['model']['cellNumberX'] = 1
        configuration['model']['cellNumberY'] = 1
        configuration['model']['cellNumberZ'] = 1
        configuration['model']['cornerPoint1'] = [0, 0, 0]
        configuration['model']['cornerPoint2'] = [1, 0, 0]

        configuration['model']['structureWidth'] = {}

        configuration['model']['structureRank'] = {}

        configuration['structure'] = {}
        configuration['structure']['file'] = []
        configuration['structure']['extension'] = []
        configuration['structure']['type'] = []


        self.writeConfigurationFromSessionStateIntoFile(configuration)

        return configuration['config']['file']


    def createJsonFile(self, configuration):
        with open(
            self.globals.default['uploadPath'] + configuration['config']['file'], 'w'
        ) as fileHandle:
            fileHandle.write(json.dumps(configuration))


    def createYamlFile(self, configuration):
        with open(
            self.globals.default['uploadPath'] + \
                configuration['config']['file'].split(".")[0] + ".yaml", 'w'
        ) as fileHandle:
            fileHandle.write(yaml.dump(configuration))


    def createStructureFile(self, file, label='layer'):
        if 'structure' not in st.session_state.configuration:
            st.session_state.configuration['structure'] = {}

        if 'file' not in st.session_state.configuration['structure']:
            st.session_state.configuration['structure']['file'] = []

        if 'extension' not in st.session_state.configuration['structure']:
            st.session_state.configuration['structure']['extension'] = []

        if 'type' not in st.session_state.configuration['structure']:
            st.session_state.configuration['structure']['type'] = []


        byteData = file.read()

        with open(self.globals.default['uploadPath']  + file.name, "wb+") as fileHandle:
            if file.name not in st.session_state.configuration['structure']['file']:
                st.session_state.configuration['structure']['file'].append(file.name)
                st.session_state.configuration['structure']['extension'].append(
                    '.' + file.name.split('.')[1]
                )
                st.session_state.configuration['structure']['type'].append(label)
                fileHandle.write(byteData)


                if label == 'fault':
                    st.session_state.configuration['model'][
                        'structureWidth'
                    ][file.name.split(".")[0]] = 1

                st.session_state.configuration['model'][
                    'structureRank'
                ][file.name.split(".")[0]] = 0


    def writeConfigurationFromSessionStateIntoFile(self, configuration):
        self.createJsonFile(configuration)
        self.createYamlFile(configuration)


    def discretisationFormHandle(self):
        if 'model' in st.session_state.configuration:
            if 'discretisationType' in st.session_state.configuration['model']:
                st.session_state['discretisationType'] = \
                st.session_state.configuration['model']['discretisationType']

            dx = [1,1,1]
            dy = [1,1,1]
            dz = [1,1,1]

            if 'discretisationX' in st.session_state.configuration['model']:
                    dx = st.session_state.configuration['model']['discretisationX']

            if 'discretisationY' in st.session_state.configuration['model']:
                    dy = st.session_state.configuration['model']['discretisationY']

            if 'discretisationZ' in st.session_state.configuration['model']:
                    dz = st.session_state.configuration['model']['discretisationZ']

            st.session_state.discretisationDiscret = pd.DataFrame.from_dict(
                dict(
                    dx=dx,
                    dy=dy,
                    dz=dz
                ),
                orient='index'
            ).transpose()

            nx = 1
            ny = 1
            nz = 1

            if 'cellNumberX' in st.session_state.configuration['model']:
                nx = st.session_state.configuration['model']['cellNumberX']

            if 'cellNumberY' in st.session_state.configuration['model']:
                ny = st.session_state.configuration['model']['cellNumberY']

            if 'cellNumberZ' in st.session_state.configuration['model']:
                nz = st.session_state.configuration['model']['cellNumberZ']

            st.session_state.discretisationContinous = \
                f"{nx}," + \
                f"{ny}," + \
                f"{nz}"


    @staticmethod
    def cloneDirectoryContentToDestination(
        sourceDirectory,
        destinationDirectory,
        onlyFilesWithExtension
    ):

        if not os.path.isdir(sourceDirectory):
            st.warning("Change directory path of \"defaultPath\" in Globals.py to an " \
                "existing Geomodelator project!")
            st.stop()

        if not os.path.isdir(destinationDirectory):
            st.warning("Change directory path of \"uploadPath\" in Globals.py to an " \
                "existing Geomodelator project!")
            st.stop()

        for root, _, fileList in os.walk(sourceDirectory):
            for file in fileList:
                if file.split('.')[1] in onlyFilesWithExtension:
                    sourceFile = os.path.join(root, file)
                    destinationFile = os.path.join(destinationDirectory, file)
                    shutil.copyfile(sourceFile, destinationFile)


    def btnApiGmlConfigure(self) -> None:
        st.session_state.btnApiGmlConfigure = True


    def btnApiGmlRun(self) -> None:
        self.btnApiGmlConfigure()
        st.session_state.wizardWindow = False
        st.session_state.btnApiGmlRun = True

    def btnShow(self) ->None:
        st.session_state.wizardWindow = False


    def btnApiWizardRun(self, state='clean') -> None:
        st.session_state.wizardWindow = True
        if state == 'clean':
            st.session_state.btnApiGmlConfigure = False
            st.session_state.btnApiGmlRun = False
        elif state == 'modelType':
            st.session_state.wizardSteps = self.globals.wizard['TypeOfModel']['wizardId']
        elif state == 'loadLayers':
            st.session_state.wizardSteps = self.globals.wizard['LoadLayers']['wizardId']
        elif state == 'loadFaults':
            st.session_state.wizardSteps = self.globals.wizard['LoadOtherStructures']['wizardId']
        elif state == 'loadMask':
            st.session_state.wizardSteps = self.globals.wizard['LoadMask']['wizardId']
        elif state == 'setModelParameter':
            st.session_state.wizardSteps = self.globals.wizard['SetModelParameter']['wizardId']
        elif state == 'setDiscretisation':
            st.session_state.wizardSteps = self.globals.wizard['SetDiscretisation']['wizardId']
        elif state == 'setStructureWidth':
            st.session_state.wizardSteps = self.globals.wizard['SetStructureWidth']['wizardId']
        elif state == 'setStructureRank':
            st.session_state.wizardSteps = self.globals.wizard['SetStructureRank']['wizardId']


    @staticmethod
    def cleanDirectory(directory):
        filesList= glob.glob(directory + '*')
        for file in filesList:
            try:
                os.remove(file)
            except:
                pass


    @staticmethod
    def reload():
        st.session_state.btnApiGmlConfigure = False
        st.session_state.btnApiGmlRun = False
        st.session_state.stateApiGmlRun = True


    @staticmethod
    def tearDown():
        st.session_state.btnApiGmlConfigure = False
        st.session_state.btnApiGmlRun = False
        st.session_state.stateApiGmlRun = False