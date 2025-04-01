# SPDX-FileCopyrightText: 2025 Benjamin Nakaten (GFZ) <bnakaten@gfz-potsdam.de>
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
#
# SPDX-License-Identifier: GPL-3.0-only

import numpy as np
import zipfile
import yaml


from pyevtk.hl import gridToVTK

import matplotlib as mpl
import matplotlib.pyplot as plt

import logging

import importlib
gml = importlib.import_module("geomodelator.gml")


class gmlRunMapper():

    def __init__(self, runSettings):
        self.settings = runSettings

    def generateModel(self):

        model = gml.Model(self.settings.gml_rs)

        model.generateGridPoints()

        cellCenterModel = gml.CenterPointModel(self.settings.gml_rs)
        cellCenterModel.generateGridPoints(model)

        uploaded_files = self.settings.gml_rs.structureFileList
        uploaded_types = self.settings.gml_rs.structureTypeList

        partitioning = gml.Partitioning(cellCenterModel)

        layers, layer_elevs = partitioning.partitionateModel(
            model=cellCenterModel,
            structureType='layer',
            filenameList=uploaded_files,
            filenameType=uploaded_types
        )
        faults, fault_elevs = partitioning.partitionateModel(
            model=cellCenterModel,
            structureType='fault',
            filenameList=uploaded_files,
            filenameType=uploaded_types
        )


        def sortLayerList(layers):
            layerModeList = []
            for index, value in enumerate(layers.A):
                a = layers.A[index]
                layerModeList.append(
                    [layers.A[index]['option'], layers.A[index]['name'], index]
                )

            layerModeList.sort(key=lambda x: x[0], reverse=True)

            layersTmp = gml.StructureList()
            layersTmp.A = {}
            layersTmp.B = {}
            layersTmp.orientation = {}
            layersTmp.type = {}
            layersTmp.id = 0
            i = 0

            for layerMode in layerModeList:

                layersTmp.A[i] = layers.A[layerMode[2]]
                layersTmp.orientation[i] = layers.orientation[layerMode[2]]
                layersTmp.type[i] = layers.fileType[layerMode[2]]
                layersTmp.id = layers.id

                i += 1

            return layersTmp


        layers = sortLayerList(layers)

        layersN = len(layers.A)
        for index, value in enumerate(faults.A):
            layers.A[layersN] = faults.A[index]
            layers.orientation[layersN] = faults.orientation[index]
            layers.type[layersN] = faults.fileType[index]
            layersN += 1

        partitioning = gml.Partitioning(cellCenterModel)

         # mask the model into active and inactive zones by using a shapefile
        all_model_data, active_model_data = partitioning.generateActivePartition(
            cellCenterModel,
            name='active',
            filenameList=uploaded_files,
            filenameType=uploaded_types
        )

        # identify partitions an get a 3d data array
        all_model_data, partition_model_data, fault_model_data = \
            partitioning.GenerateLayerPartitions(
                cellCenterModel,
                layers,
                old_grid_data=active_model_data
            )

        cell_ids, i_ids, j_ids, k_ids = partitioning.generateModelCellIds(cellCenterModel)

        vtk_grid_x, vtk_grid_y, vtk_grid_z = partitioning.rotateModel(model)

        gridToVTK(
            cellCenterModel.configuration.outputPath + 'model',
            vtk_grid_x,
            vtk_grid_y,
            vtk_grid_z,
            cellData = {
                'cell_ids': cell_ids,
                'all': all_model_data,
                'partitions': partition_model_data,
                'faults': fault_model_data,
                'active': active_model_data,
                'i': i_ids,
                'j': j_ids,
                'k': k_ids
            }
        )

        self.settings.rs['model']['partitionId'] = cellCenterModel.configuration.part

        cmap = plt.get_cmap('tab20')
        colors = [mpl.colors.rgb2hex(cmap(i)) for i in range(cmap.N)]
        pnames = []
        pvalues = []
        pshow = []
        i = 0
        for part in self.settings.rs['model']['partitionId'].keys():
            if part == 'all':
                pnames.append(part)
                pvalues.append('#ffffff')
                pshow.append(False)

            else:
                pnames.append(part)
                pvalues.append(colors[i%cmap.N])
                pshow.append(True)
                i += 2

        self.settings.rs['gui'] = {}
        self.settings.rs['gui']['partitionColor'] = dict(
            partition = pnames,
            color = pvalues,
            show = pshow
        )

        cmap = plt.get_cmap('tab20')
        colors = [mpl.colors.rgb2hex(cmap(i)) for i in range(cmap.N)]
        pnames = []
        pvalues = []
        pshow = []

        i = 0
        for part in self.settings.rs['structure']['file']:
            pnames.append(part.split('.')[0])
            pvalues.append(colors[(i+10)%cmap.N])
            pshow.append(True)
            i += 2

        self.settings.rs['gui']['surfaceColor'] = dict(
            surface = pnames,
            color = pvalues,
            show = pshow
        )


        FILENAME = cellCenterModel.configuration.outputPath+'model_all_data_numpy_array'
        np.savez_compressed(FILENAME, array1=all_model_data, cell_ids=cell_ids)

        logging.info("====================================")
        logging.info('Run successful! \U0001f37b\n')


        if self.settings.rs['config']['csv']['compress'] :
            Compress(self.settings.rs)

        self.settings.rs['run'] = True

        model_run_data = self.settings.rs

        return model_run_data


class Compress:
    def __init__(self, rs):
        compression = zipfile.ZIP_DEFLATED

        input_path = rs['config']['base'] + rs['config']['inputPath']
        output_path = rs['config']['base'] + rs['config']['outputPath']

        zfile = 'Model.zip'
        zf = zipfile.ZipFile(output_path + zfile, mode='w')

        for i, file in enumerate(rs['structure']['file']):
            if rs['structure']['extension'][i] == '.csv' or \
                rs['structure']['extension'][i] == '.asc':
                filename = file.split('.')[0]+'.vtk'
                try:
                    zf.write(output_path + filename, filename, compress_type=compression)
                except:
                    pass

        filename = rs['config']['modelFileVtk']
        zf.write(output_path + filename, filename, compress_type=compression)

        filename = 'model_all_data_numpy_array.npz'
        zf.write(output_path + filename, filename, compress_type=compression)

        zf.close()

        zfile = 'Configuration.zip'
        zf = zipfile.ZipFile(input_path + zfile, mode='w')

        filename = rs['config']['file']
        zf.write(input_path + filename, filename, compress_type=compression)

        fileExtension = rs['config']['file'].split('.')[-1]

        filename = rs['config']['file'].split('.')[0] + (
            '.yaml' if fileExtension == 'json' else '.json'
        )
        with open(input_path + filename, 'w') as f:
            yaml.dump(rs, f)

        zf.write(input_path + filename, filename, compress_type=compression)

        for filename in rs['structure']['file']:
            zf.write(input_path + filename, filename, compress_type=compression)

        zf.close()
