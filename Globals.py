class Globals():

    default = {
        'logo' : 'geomodelatorgui_logo_name.png',
        'apiBaseUrl' : 'http://localhost:5000/api/gml/',
        'defaultPath' : 'static/demo/',
        'uploadPath'  : 'static/tmp/',
        'configurationFileName' : 'configuration',
        'modelFileVtk' : 'model.vts',
        'stpyvistaBackgroundColor' : '#ffffff',
    }

    info = {
        'configurationFileExtensions' : ['yaml', 'json'],
        'pointCloudFileExtensions' : ['csv', 'asc'],
        'shapeFileExtensions' : ['dbf', 'prj', 'qmd', 'shp', 'shx'],
    }

    wizard = {
        'mainHeadline' : 'Model configuration',
        'nextButton' : 'Next',
        'backButton' : 'Back',
        'startButton' : 'Start',
        'demoButton' : 'Demo',
        'customButton' : 'Custom',
        'resetButton' : 'Reset',
        'runButton' : 'Update model',
        'DemoOrCustom' : {
            'header' : 'Run the demo or setup your custom model',
            'image' : 'images/geomodelator_animination.gif',
        },
        'TypeOfModel' : {
            'header' : '',
            'image' : 'images/2dplusOr3d.png',
            'radioButton' : {
                'text' : 'Choose model type:',
                'option1Text' : '2.5D',
                'option2Text' : '3D',
                'caption1' : '2D point clouds extruded into y-direction',
                'caption2' : '3D model from point clouds',
            },
            'wizardId' : 1
        },
        'LoadLayers' : {
            'header' : 'Load layer surface point clouds',
            'descriptionText' : 'Point cloud must not be coplanar',
            'descriptionHelper' : 'A set of points in space are coplanar if there exists a geometric plane that contains them all',
            'image' : 'images/layer3d-result.png',
            'fileUploaderText' : '',
            'previousUploadedFilesText' : 'Previous uploaded files:',
            'deleteFileButton' : 'Delete',
            'wizardId' : 2
        },
        'LoadOtherStructures' : {
            'header' : 'Load fault surface point clouds',
            'descriptionText' : 'Point cloud must not be coplanar',
            'descriptionHelper' : 'A set of points in space are coplanar if there exists a geometric plane that contains them all',
            'image' : 'images/fault3d-result.png',
            'fileUploaderText' : '',
            'previousUploadedFilesText' : 'Previous uploaded files:',
            'deleteFileButton' : 'Delete',
            'wizardId' : 3
        },
        'LoadMask' : {
            'header' : 'Load boundary point cloud',
            'descriptionText' : 'Convex polygon created from the point cloud forms the boundaries of the mask',
            'descriptionHelper' : 'A convex polygon is any shape that has all interior angles that measure less than 180 degrees',
            'image' : 'images/mask-good-bad.png',
            'fileUploaderText' : '',
            'previousUploadedFilesText' : 'Previous uploaded files:',
            'modelDimensionInfo' : """The point cloud is interpreted as a convex xy-mask, which which then cuts out all model cells that are not covered by the point cloud and sets these cells to inactive. In addition, the point cloud need at least 3 points which are not not coplanar (not located on a single line)!""",
            'deleteFileButton' : 'Delete',
            'wizardId' : 4
        },
        'SetModelParameter' : {
            'header' : '',
            'descriptionText' : '',
            'descriptionHelper' : '',
            'image' : 'images/gml-help-model-corners-and-size.png',
            'cornerPoint1Text' : 'Corner point 1 (m):',
            'cornerPoint2Text' : ' Corner point 2 (m):',
            'modelDimension' : ' Model dimension (size)',
            'modelDimensionXText' : 'x (m):',
            'modelDimensionYText' : 'y (m):',
            'modelDimensionZText' : 'z (m):',
            'modelDimensionInfo' : 'The second corner point is only considered to calculate the translation of a model with rotation, in contrast to a rectangular normal orientation of a model.',
            'modelDimensionValueError' : 'Only  integer values are allowed!',
            'modelDimensionOverflowError' : 'The tuple should consist of excatly 3 items (x,y,z)!',
            'saveButton' : 'Save',
            'wizardId' : 5
        },
        'SetDiscretisation' : {
            'header' : 'Discretisation',
            'image' : 'images/gml-help-model-gridding.png',
            'toggleButton' : 'Constant',
            'typeTextDiscret' : 'Tartan',
            'typeTextConstant' : 'Constant',
            'textInputConstant': 'nx,ny,nz:',
            'textInputDiscret' : 'The unit of discretisation is equal to the unit of the model dimensions. The sum of the discretisation values for each direction must not exceed the model dimension. The sum of the individual directions must be equal to or less than the dimension in the respective direction.',
            'errorDx' : 'Model dimension is to small for the discretisation, Please\nchange model dimension x value or discretisation dx values.',
            'errorDy' : 'Model dimension is to small for the discretisation, Please\nchange model dimension y value or discretisation dy values.',
            'errorDz' : 'Model dimension is to small for the discretisation, Please\nchange model dimension z value or discretisation dz values.',
            'modelDiscretisationValueError' : 'Only  integer values are allowed!',
            'modelDiscretisationOverflowError' : 'The tuple should consist of excatly 3 items (x,y,z)!',
            'saveButton' : 'Save',
            'wizardId' : 6
        },
        'SetStructureWidth' : {
            'header' : '',
            'image' : 'images/gml-fault-width.png',
            'saveButton' : 'Save',
            'wizardId' : 7
        },
        'SetStructureRank' : {
            'header' : 'Surface priority',
            'image' : 'images/model-layer-fault-rang.png',
            'saveButton' : 'Save',
            "textInfo" : "The higher the rank, the more relevant the surface of the structure is. If, for example, there is a layer surface with rank 2 and fault surface with rank 1, the fault part above the layer surface is cut off.",
            'wizardId' : 8
        },
    }

    viewTab = {
        'plot' : ':desktop_computer: ANALYSE',
        'parameter' : ':gear: EDIT',
        'download' : ':paperclip: EXPORT',
    }

    button = {
        'wizard' : 'Wizard',
        'show' : 'Update view',
        'download' : {
            'outputFilenameLable' : 'Model',
            'inputFilenameLable' : 'Configuration',
        }
    }

    file = {
        'download' : {
            'outputFilename' : 'Model.zip',
            'inputFilename' : 'Configuration.zip',
        }
    }

    viewControl = {
        'zAxisScale' : {
            'descriptionLable' : 'Scale z-axis',
            'min' : 0.0,
            'step' : 0.1,
            'max' : 100.0,
            'default' : 1,
            'help' : 'Use the arrow keys to set the slider in increments of 0.1, and the image up or image down keys to adjust in increments of 1.'

        },
        'modelOpacity' : {
            'descriptionLable' : 'Model opacity',
            'min' : 0.0,
            'step' : 0.2,
            'max' : 1.0,
            'default' : 1.0,

        },
        'modelWireframe' : {
            'descriptionLable' : 'Wireframe',
            'default' : True,
        },
        'modelHide' : {
            'descriptionLable' : 'Model',
            'default' : False,
        },
        'partitionTable' : {
            'columnNames' :  ['Partition', 'Id', 'Color']
        },
        'surfaceTable' : {
            'columnNames' :  ['Surface', 'Id', 'Color']
        },
        'surfaceOpacity' : {
            'descriptionLable' : 'Structure opacity',
            'min' : 0.0,
            'step' : 0.2,
            'max' : 1.0,
            'default' : 0.6,

        },
        'surfaceWireframe' : {
            'descriptionLable' : 'Wireframe',
            'default' : False,
        },
        'surfaceHide' : {
            'descriptionLable' : 'Structure',
            'default' : False,
        },
        'backgroundColor' :{
            'descriptionLable' : 'Background',
            'color' : '#ffffff',
        }
    }

    EditParameter = {
        'modelType' : 'Model type:',
        'dimension' : 'Dimension (m):',
        'cornerPoint1' : 'Corner point 1:',
        'cornerPoint2' : 'Corner point 2:',
        'discretisationType' : 'Discretisation type: ',
        'discretisationConstant' : 'Cell number x-, y-, z-direction',

    }

    ModelPlotter = {
        'loadingSpinnerText' : 'Visualize ...',
        'error' : {
            'plotterData' : 'There was an error in plotter data. Please, try again.',
            'somethingHasGoneWrong' : 'Something has gone wrong!',
            'couldNotbeFound' : 'could not be found!',
        },
        'width' : 1000,
        'height' : 800,
        'backgroundColor' : 'white',
        'legendColorbar' : 2.2,
        'infoTextNavigation' : '- Press *<shift> + left mouse button* and use the mouse to move model in plotting view\n- Use *mouse wheel* to zoom in and out\n- Press *left mouse button* to rotate the model\n- In main plot window click the "..." to show the legend',
    }