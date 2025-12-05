#!/usr/bin/env python3
"""
Script para testar a correção do problema de carregamento de arquivos NetCDF
"""

import os
import sys
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geonode.settings')
django.setup()

from geonode.upload.handlers.netcdf.handler import NetCDFFileHandler
import tempfile
import netCDF4
import numpy as np

def create_test_netcdf():
    """Cria um arquivo NetCDF de teste"""
    temp_file = tempfile.NamedTemporaryFile(suffix='.nc', delete=False)
    
    with netCDF4.Dataset(temp_file.name, 'w') as nc:
        # Create dimensions
        nc.createDimension('time', 10)
        nc.createDimension('lat', 180)
        nc.createDimension('lon', 360)
        
        # Create variables
        time_var = nc.createVariable('time', 'f4', ('time',))
        lat_var = nc.createVariable('lat', 'f4', ('lat',))
        lon_var = nc.createVariable('lon', 'f4', ('lon',))
        temp_var = nc.createVariable('temperature', 'f4', ('time', 'lat', 'lon'))
        
        # Add data
        time_var[:] = np.arange(10)
        lat_var[:] = np.linspace(-90, 90, 180)
        lon_var[:] = np.linspace(-180, 180, 360)
        temp_var[:] = np.random.rand(10, 180, 360)
        
        # Add attributes
        time_var.units = 'days since 2000-01-01'
        lat_var.units = 'degrees_north'
        lon_var.units = 'degrees_east'
        temp_var.units = 'celsius'
        temp_var.long_name = 'Temperature'
        
        # Global attributes
        nc.title = 'Test NetCDF Dataset'
        nc.description = 'A test NetCDF file for testing the fix'
        nc.crs_wkt = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'
    
    return temp_file.name

def test_netcdf_handler():
    """Testa o handler NetCDF corrigido"""
    print("🧪 Testando o handler NetCDF corrigido...")
    
    # Criar arquivo de teste
    test_file = create_test_netcdf()
    print(f"✓ Arquivo de teste criado: {test_file}")
    
    try:
        # Testar o handler
        handler = NetCDFFileHandler()
        
        # Testar extração de CRS
        crs = handler._extract_crs_from_netcdf(test_file)
        print(f"✓ CRS extraído: {crs}")
        
        # Testar extração de metadados
        metadata = handler.extract_netcdf_metadata(test_file)
        print(f"✓ Metadados extraídos: {metadata['title']}")
        
        # Testar extract_resource_to_publish
        files = {'base_file': test_file}
        resources = handler.extract_resource_to_publish(
            files=files,
            action='upload',
            layer_name='test_layer',
            alternate='test_alternate'
        )
        print(f"✓ Recursos para publicação: {resources}")
        
        print("\n✅ Todos os testes passaram! O handler NetCDF está funcionando corretamente.")
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Limpar arquivo de teste
        os.unlink(test_file)
        print(f"✓ Arquivo de teste removido: {test_file}")

if __name__ == '__main__':
    test_netcdf_handler()

