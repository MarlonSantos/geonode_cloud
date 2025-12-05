#!/usr/bin/env python3
"""
Script para testar se o método extract_resource_to_publish está sendo sobrescrito corretamente
"""

import os
import sys
import django
import tempfile
import netCDF4
import numpy as np

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geonode.settings')
django.setup()

from geonode.upload.handlers.netcdf.handler import NetCDFFileHandler
from geonode.upload.handlers.common.raster import BaseRasterFileHandler

def create_test_netcdf():
    """Cria um arquivo NetCDF de teste"""
    temp_file = tempfile.NamedTemporaryFile(suffix='.nc', delete=False)
    
    with netCDF4.Dataset(temp_file.name, 'w') as nc:
        # Create dimensions
        nc.createDimension('time', 5)
        nc.createDimension('lat', 90)
        nc.createDimension('lon', 180)
        
        # Create variables
        time_var = nc.createVariable('time', 'f4', ('time',))
        lat_var = nc.createVariable('lat', 'f4', ('lat',))
        lon_var = nc.createVariable('lon', 'f4', ('lon',))
        temp_var = nc.createVariable('temperature', 'f4', ('time', 'lat', 'lon'))
        
        # Add data
        time_var[:] = np.arange(5)
        lat_var[:] = np.linspace(-90, 90, 90)
        lon_var[:] = np.linspace(-180, 180, 180)
        temp_var[:] = np.random.rand(5, 90, 180)
        
        # Add attributes
        time_var.units = 'days since 2000-01-01'
        lat_var.units = 'degrees_north'
        lon_var.units = 'degrees_east'
        temp_var.units = 'celsius'
        temp_var.long_name = 'Temperature'
        
        # Global attributes
        nc.title = 'Test NetCDF for method override'
        nc.description = 'A test NetCDF file for testing method override'
        nc.epsg = "ESPG4326"  # Problema que queremos corrigir
    
    return temp_file.name

def test_method_override():
    """Testa se o método extract_resource_to_publish está sendo sobrescrito"""
    print("🔍 Testando sobrescrita do método extract_resource_to_publish...")
    
    # Criar arquivo de teste
    test_file = create_test_netcdf()
    print(f"✓ Arquivo de teste criado: {test_file}")
    
    try:
        # Testar BaseRasterFileHandler (classe pai)
        print(f"\n1. Testando BaseRasterFileHandler...")
        base_handler = BaseRasterFileHandler()
        
        # Verificar se tem o método
        if hasattr(base_handler, 'extract_resource_to_publish'):
            print("   ✅ BaseRasterFileHandler tem método extract_resource_to_publish")
            
            # Verificar o método
            import inspect
            method = getattr(base_handler, 'extract_resource_to_publish')
            method_source = inspect.getsource(method)
            
            if 'gdal.Open' in method_source:
                print("   ✅ BaseRasterFileHandler usa gdal.Open")
            else:
                print("   ❌ BaseRasterFileHandler NÃO usa gdal.Open")
        else:
            print("   ❌ BaseRasterFileHandler NÃO tem método extract_resource_to_publish")
        
        # Testar NetCDFFileHandler (nossa classe)
        print(f"\n2. Testando NetCDFFileHandler...")
        netcdf_handler = NetCDFFileHandler()
        
        # Verificar se tem o método
        if hasattr(netcdf_handler, 'extract_resource_to_publish'):
            print("   ✅ NetCDFFileHandler tem método extract_resource_to_publish")
            
            # Verificar o método
            method = getattr(netcdf_handler, 'extract_resource_to_publish')
            method_source = inspect.getsource(method)
            
            if '_extract_crs_from_netcdf' in method_source:
                print("   ✅ NetCDFFileHandler usa _extract_crs_from_netcdf")
            else:
                print("   ❌ NetCDFFileHandler NÃO usa _extract_crs_from_netcdf")
                
            if 'gdal.Open' in method_source:
                print("   ❌ NetCDFFileHandler ainda usa gdal.Open (não foi sobrescrito)")
            else:
                print("   ✅ NetCDFFileHandler NÃO usa gdal.Open (foi sobrescrito)")
        else:
            print("   ❌ NetCDFFileHandler NÃO tem método extract_resource_to_publish")
        
        # Testar se os métodos são diferentes
        print(f"\n3. Comparando métodos...")
        base_method = getattr(base_handler, 'extract_resource_to_publish')
        netcdf_method = getattr(netcdf_handler, 'extract_resource_to_publish')
        
        if base_method == netcdf_method:
            print("   ❌ Métodos são iguais (não foi sobrescrito)")
        else:
            print("   ✅ Métodos são diferentes (foi sobrescrito)")
        
        # Testar execução do método
        print(f"\n4. Testando execução do método...")
        files = {'base_file': test_file}
        action = 'upload'
        layer_name = 'test_layer'
        alternate = 'test_alternate'
        
        try:
            resources = netcdf_handler.extract_resource_to_publish(
                files=files,
                action=action,
                layer_name=layer_name,
                alternate=alternate
            )
            
            print(f"   ✅ Método executado com sucesso")
            print(f"   - Número de recursos: {len(resources)}")
            
            for i, resource in enumerate(resources):
                print(f"   - Recurso {i+1}:")
                print(f"     - name: {resource.get('name')}")
                print(f"     - crs: {resource.get('crs')}")
                print(f"     - raster_path: {resource.get('raster_path')}")
                
                # Verificar se o CRS está correto
                crs = resource.get('crs')
                if crs == "EPSG:4326":
                    print(f"     ✅ CRS correto: {crs}")
                else:
                    print(f"     ❌ CRS incorreto: {crs}")
                    print(f"     - Esperado: EPSG:4326")
                    print(f"     - Recebido: {crs}")
            
            return resources
            
        except Exception as e:
            print(f"   ❌ Erro na execução: {e}")
            import traceback
            traceback.print_exc()
            return None
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        # Limpar arquivo de teste
        os.unlink(test_file)
        print(f"\n✓ Arquivo de teste removido: {test_file}")

if __name__ == '__main__':
    print("🔧 Teste de Sobrescrita do Método extract_resource_to_publish")
    print("=" * 70)
    
    # Testar sobrescrita do método
    result = test_method_override()
    
    print(f"\n📋 Resumo:")
    if result:
        print(f"   ✅ Método extract_resource_to_publish foi sobrescrito corretamente")
        print(f"   ✅ Método está funcionando e corrigindo o CRS")
    else:
        print(f"   ❌ Há problemas com a sobrescrita do método")
        print(f"   ❌ O método pode não estar sendo chamado corretamente")
    
    print(f"\n💡 Se o método foi sobrescrito mas o erro persiste,")
    print(f"   o problema pode estar em outro lugar do fluxo.")

