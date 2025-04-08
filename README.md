<!--
SPDX-FileCopyrightText: 2025 Benjamin Nakaten (GFZ) <bnakaten@gfz-potsdam.de>
SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences

SPDX-License-Identifier: CC-BY-4.0
-->

[![DOI:10.5880/GFZ.AJPH.2025.002](https://img.shields.io/badge/DOI-10.5880%2FGFZ.AJPH.2025.002-blue.svg)](https://doi.org/10.5880/GFZ.AJPH.2025.002)
[![DOI:10.5880/GFZ.AJPH.2025.001](https://img.shields.io/badge/DOI-10.5880%2FGFZ.AJPH.2025.001-blue.svg)](https://doi.org/10.5880/GFZ.AJPH.2025.001)


# GeomodelatorGUI

A graphical user interface (GUI) based on python, streamlit and pyvista to use the free
[GEOMODELATOR](https://git.gfz.de/bnakaten/geomodelator) to setup 3d geolocial models for
the simulator framework [TRANSPORTSE](https://git.gfz.de/kempka/transportse).

[Visit Wiki](https://git.gfz.de/bnakaten/geomodelator/-/wikis)

![GEOMODELATOR GUI](geomodelatorgui_logo_name.png "GEOMODELATOR GUI")


# Requirements

**GeomodelatorGUI** requires the following packages and is restricted to those specified in environment.yml.:
  - python
  - flask
  - gdal
  - geos
  - matplotlib
  - numpy
  - pandas
  - pip
  - pyevtk
  - pyyaml
  - pyvista
  - scipy
  - streamlit
  - stpyvista

> On Debian/Ubunut install procps, libgl1-mesa-glx and xvfb for the packages pyvista and stpyvista.

> ```
> sudo apt install procps libgl1-mesa-glx xvfb
>```

# I) Installation

1. Download **GeomodelatorGUI**.

    ```
    git clone https://git.gfz.de/bnakaten/geomodelatorGUI

    #git -c http.sslVerify=false  clone https://git.gfz.de/bnakaten/geomodelatorGUI

    cd GeomodelatorGUI

    git checkout tags/v1.0

    git submodule update --init --recursive
    ```

2. Setup conda envrionment conda.

    ```
    mamba env create -f environment.yml

    mamba activate gmlGUI
    ```

# II) Use GeomodelatorGUI

1. Start the GEOMODELATOR server module.

    ```
    python gmlPort.py
    ```

2. Start the GeomodelatorGUI.

    ```
    streamlit run geomodelatorGui.py
    ```

    The GeomodelatorGUI opens in the web browser.

3. Further details can be found in the [GeomodelatorGUI Wiki](https://git.gfz.de/bnakaten/geomodelatorgui/-/wikis) or in the [GEOMODELATOR Wiki](https://git.gfz.de/bnakaten/geomodelator/-/wikis)

# License and Copyright

Copyright 2025 GFZ Helmholtz Centre for Geosciences.

The code in this repository is licensed GPL-3.0-only.

For detailed license information, refer to the file headers or the REUSE.toml file. All license terms are available in the LICENSES directory.
