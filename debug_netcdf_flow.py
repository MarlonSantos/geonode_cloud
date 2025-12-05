#!/usr/bin/env python3
"""
Script para debugar o fluxo completo de upload de NetCDF
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

def create_test_netcdf_with_problematic_crs():
    """Cria um arquivo NetCDF que pode causar o erro ESPG4326"""
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
        
        # Global attributes - SIMULAR O PROBLEMA
        nc.title = 'Test NetCDF with problematic CRS'
        nc.description = 'A test NetCDF file that may cause ESPG4326 error'
        
        # Adicionar CRS problemático (simulando o que pode estar no arquivo real)
        nc.epsg = "ESPG4326"  # Este é o problema!
        
        # Também adicionar um CRS correto para comparação
        nc.crs = "EPSG:4326"
    
    return temp_file.name

def debug_extract_resource_to_publish():
    """Debuga o método extract_resource_to_publish"""
    print("🔍 Debugando extract_resource_to_publish...")
    
    # Criar arquivo de teste
    test_file = create_test_netcdf_with_problematic_crs()
    print(f"✓ Arquivo de teste criado: {test_file}")
    
    try:
        handler = NetCDFFileHandler()
        
        # Simular dados de entrada
        files = {'base_file': test_file}
        action = 'upload'
        layer_name = 'test_layer'
        alternate = 'test_alternate'
        
        print(f"\n📋 Parâmetros de entrada:")
        print(f"   - base_file: {test_file}")
        print(f"   - action: {action}")
        print(f"   - layer_name: {layer_name}")
        print(f"   - alternate: {alternate}")
        
        # Chamar o método
        print(f"\n🚀 Chamando extract_resource_to_publish...")
        resources = handler.extract_resource_to_publish(
            files=files,
            action=action,
            layer_name=layer_name,
            alternate=alternate
        )
        
        print(f"\n📊 Resultado:")
        print(f"   - Número de recursos: {len(resources)}")
        
        for i, resource in enumerate(resources):
            print(f"\n   Recurso {i+1}:")
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
        print(f"❌ Erro durante o debug: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        # Limpar arquivo de teste
        os.unlink(test_file)
        print(f"\n✓ Arquivo de teste removido: {test_file}")

def debug_crs_extraction_directly():
    """Debuga a extração de CRS diretamente"""
    print(f"\n🔍 Debugando extração de CRS diretamente...")
    
    # Criar arquivo de teste
    test_file = create_test_netcdf_with_problematic_crs()
    print(f"✓ Arquivo de teste criado: {test_file}")
    
    try:
        handler = NetCDFFileHandler()
        
        # Testar extração de CRS diretamente
        print(f"\n🚀 Chamando _extract_crs_from_netcdf...")
        crs = handler._extract_crs_from_netcdf(test_file)
        
        print(f"\n📊 Resultado da extração de CRS:")
        print(f"   - CRS extraído: '{crs}'")
        print(f"   - Tipo: {type(crs)}")
        print(f"   - Tamanho: {len(crs)}")
        
        # Verificar se está correto
        if crs == "EPSG:4326":
            print(f"   ✅ CRS correto!")
        else:
            print(f"   ❌ CRS incorreto!")
            print(f"   - Esperado: EPSG:4326")
            print(f"   - Recebido: {crs}")
        
        # Testar normalização diretamente
        print(f"\n🧪 Testando normalização diretamente...")
        test_cases = ["ESPG4326", "EPSG:4326", "4326", "epsg:4326"]
        
        for test_case in test_cases:
            normalized = handler._normalize_crs(test_case)
            print(f"   - {test_case} -> {normalized}")
        
        return crs
        
    except Exception as e:
        print(f"❌ Erro durante o debug: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        # Limpar arquivo de teste
        os.unlink(test_file)
        print(f"\n✓ Arquivo de teste removido: {test_file}")

def check_handler_registration():
    """Verifica se o handler está registrado corretamente"""
    print(f"\n🔍 Verificando registro do handler...")
    
    try:
        from geonode.upload.settings import SYSTEM_HANDLERS
        
        print(f"   - SYSTEM_HANDLERS encontrado")
        print(f"   - Número de handlers: {len(SYSTEM_HANDLERS)}")
        
        # Verificar se NetCDF handler está na lista
        netcdf_handler = "geonode.upload.handlers.netcdf.handler.NetCDFFileHandler"
        
        if netcdf_handler in SYSTEM_HANDLERS:
            print(f"   ✅ NetCDF handler registrado: {netcdf_handler}")
        else:
            print(f"   ❌ NetCDF handler NÃO registrado!")
            print(f"   - Handlers registrados:")
            for handler in SYSTEM_HANDLERS:
                print(f"     - {handler}")
        
        # Verificar se pode importar o handler
        try:
            from geonode.upload.handlers.netcdf.handler import NetCDFFileHandler
            print(f"   ✅ NetCDF handler pode ser importado")
            
            # Verificar se pode instanciar
            handler = NetCDFFileHandler()
            print(f"   ✅ NetCDF handler pode ser instanciado")
            
            # Verificar se tem o método _normalize_crs
            if hasattr(handler, '_normalize_crs'):
                print(f"   ✅ Método _normalize_crs existe")
            else:
                print(f"   ❌ Método _normalize_crs NÃO existe!")
                
        except Exception as e:
            print(f"   ❌ Erro ao importar/instanciar handler: {e}")
            
    except Exception as e:
        print(f"❌ Erro ao verificar registro: {e}")

if __name__ == '__main__':
    print("🔧 Debug do Fluxo Completo de NetCDF")
    print("=" * 60)
    
    # Verificar registro do handler
    check_handler_registration()
    
    # Debugar extração de CRS diretamente
    crs_result = debug_crs_extraction_directly()
    
    # Debugar extract_resource_to_publish
    resources_result = debug_extract_resource_to_publish()
    
    print(f"\n📋 Resumo do Debug:")
    print(f"   • Handler registrado: {'✅' if 'geonode.upload.handlers.netcdf.handler.NetCDFFileHandler' in str(SYSTEM_HANDLERS) else '❌'}")
    print(f"   • Extração de CRS: {'✅' if crs_result == 'EPSG:4326' else '❌'}")
    print(f"   • extract_resource_to_publish: {'✅' if resources_result else '❌'}")
    
    if resources_result:
        for resource in resources_result:
            crs = resource.get('crs')
            if crs != "EPSG:4326":
                print(f"   ❌ CRS incorreto encontrado: {crs}")
                break
        else:
            print(f"   ✅ Todos os CRS estão corretos")
    
    print(f"\n💡 Se todos os testes passaram, o problema pode estar em outro lugar do fluxo.")
    print(f"   Verifique os logs do Django e GeoServer para mais detalhes.")

