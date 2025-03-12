import sys
import numpy as np
import pandas as pd
import json

import logging

import importlib
gml = importlib.import_module("geomodelator-backend.gml")

# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

class gmlConfigurationMapper:

    def __init__(self, runSettings):
        if type(runSettings) is dict:
            self.rs = runSettings
        else:
            self.rs = json.loads(runSettings)

        self.rs['run'] = False

    def configureModel(self):
        if 'compress' not in self.rs['config']['csv']:
            self.rs['config']['csv']['compress'] = False


        if self.rs['model']['discretisationType'] == 'd':
            discretisationX = [
                v for v in self.rs['model']['discretisationX'] if pd.notnull(v)
            ]
            discretisationY = [
                v for v in self.rs['model']['discretisationY'] if pd.notnull(v)
            ]
            discretisationZ = [
                v for v in self.rs['model']['discretisationZ'] if pd.notnull(v)
            ]
        else:
            discretisationX = np.asarray(
                [self.rs['model']['dimension'][0]/self.rs['model']['cellNumberX']]\
                *self.rs['model']['cellNumberX']
            )
            discretisationY = np.asarray(
                [self.rs['model']['dimension'][1]/self.rs['model']['cellNumberY']]\
                *self.rs['model']['cellNumberY']
            )
            discretisationZ = np.asarray(
                [self.rs['model']['dimension'][2]/self.rs['model']['cellNumberZ']]\
                *self.rs['model']['cellNumberZ']
            )

        gml_gs = gml.Configuration()

        gml_gs.csvFormat(
            columns=self.rs['config']['csv']['columns'],
            header=int(self.rs['config']['csv']['header']),
            delimiter=self.rs['config']['csv']['delimiter'],
        )

        gml_gs.modelGrid(
            modelTyp3d=self.rs['model']['3d'],
            cornerPoint1=self.rs['model']['cornerPoint1'],
            cornerPoint2=self.rs['model']['cornerPoint2'],
            modelDimension=self.rs['model']['dimension'],
            discretisationX=discretisationX,
            discretisationY=discretisationY,
            discretisationZ=discretisationZ,
            cellNumberX=self.rs['model']['cellNumberX'],
            cellNumberY=self.rs['model']['cellNumberY'],
            cellNumberZ=self.rs['model']['cellNumberZ'],
        )

        gml_gs.dataLocation(
            inputPath=self.rs['config']['base'] + '' + self.rs['config']['inputPath'],
            outputPath= self.rs['config']['base'] + '' + self.rs['config']['outputPath'],
            shapeFilePath= self.rs['config']['base'] + '' + self.rs['config']['shapePath'],
            modelFileVtk= self.rs['config']['base'] + '' + \
                self.rs['config']['outputPath'] + self.rs['config']['modelFileVtk'],
        )

        if 'structureWidth' not in self.rs['model']:
            self.rs['model']['structureWidth'] = []

        if 'structureRank' not in self.rs['model']:
            self.rs['model']['structureRank'] = []

        gml_gs.partitionDetails(
            structureWidth=self.rs['model']['structureWidth'],
            structureRank=self.rs['model']['structureRank'],

        )

        if 'structure' in self.rs:
            if 'extension' not in self.rs['structure'] or \
                self.rs['structure']['extension'] == None:
                self.rs['structure']['extension'] = []
                for file in self.rs['structure']['file']:
                    self.rs['structure']['extension'].append(file.split('.')[-1])

            gml_gs.feature(
               maskFileName='mask.tiff',
               structureFileList=self.rs['structure']['file'],
               structureTypeList=self.rs['structure']['type'],
               structureExtensionList=self.rs['structure']['extension'],
            )

            gml_gs.part =  {}
            gml_gs.partitionCounter = 0

        self.gml_rs = gml_gs