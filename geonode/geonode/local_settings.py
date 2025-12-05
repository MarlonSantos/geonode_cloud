# -*- coding: utf-8 -*-
"""
Local settings for GeoNode project.
"""

import os
from geonode.settings import *

# Adicionar suporte para formatos NetCDF e GRIB
ADDITIONAL_DATASET_FILE_TYPES = [
    {
        "id": "netcdf",
        "label": "NetCDF",
        "formats": [
            {
                "label": "NetCDF File",
                "required_ext": ["nc", "netcdf"],
                "optional_ext": [],
            }
        ],
        "actions": ["upload", "replace"],
        "type": "raster",
    },
    {
        "id": "grib",
        "label": "GRIB",
        "formats": [
            {
                "label": "GRIB File",
                "required_ext": ["grib", "grb", "grib2", "grb2"],
                "optional_ext": [],
            }
        ],
        "actions": ["upload", "replace"],
        "type": "raster",
    },
]

# Atualizar a configuração UPLOADER para incluir as novas extensões
UPLOADER = {
    "BACKEND": "geonode.importer",
    "OPTIONS": {
        "TIME_ENABLED": True,
        "MOSAIC_ENABLED": False,
    },
    "SUPPORTED_CRS": ["EPSG:4326", "EPSG:3785", "EPSG:3857", "EPSG:32647", "EPSG:32736"],
    "SUPPORTED_EXT": [
        ".shp", ".csv", ".kml", ".kmz", ".json", ".geojson", 
        ".tif", ".tiff", ".geotiff", ".gml", ".xml",
        ".nc", ".netcdf", ".grib", ".grb", ".grib2", ".grb2"
    ],
}

# Configurações específicas para NetCDF e GRIB
NETCDF_GRIB_SETTINGS = {
    "ENABLE_NETCDF": True,
    "ENABLE_GRIB": True,
    "DEFAULT_CRS": "EPSG:4326",
    "TIME_DIMENSION_ENABLED": True,
}

# Configurações de idioma
LANGUAGE_CODE = "pt-br"

LANGUAGES = (
    ('en-us', 'English'),
    ('it-it', 'Italiano'),
    ('es-es', 'Spanish'),
    ('de-de', 'German'),
    # ('pt-pt', 'Portuguese'),
    ('pt-br', 'Portuguese (Brazil)')
)