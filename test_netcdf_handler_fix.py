#!/usr/bin/env python
"""
Teste do handler NetCDF com correção automática de CRS
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Adicionar o diretório do projeto ao path
sys.path.insert(0, '/home/marlon/projetos/geonode2')

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geonode.settings')

import django
django.setup()

from geonode.upload.handlers.netcdf.handler import NetCDFFileHandler

def test_netcdf_crs_fix():
    """Testa a correção automática de CRS no handler NetCDF"""
    
    # Arquivo de teste (usar o arquivo original que está causando problema)
    test_file = "/usr/src/geonode/geonode_custom/plugins/SST_Mediterraneo.nc"
    
    if not os.path.exists(test_file):
        print(f"❌ Arquivo de teste não encontrado: {test_file}")
        return False
    
    print(f"🧪 Testando correção de CRS para: {test_file}")
    
    # Criar handler
    handler = NetCDFFileHandler()
    
    # Testar verificação de CRS
    print("\n1. Verificando se arquivo tem informações de CRS...")
    has_crs = handler._has_crs_info(test_file)
    print(f"   Tem CRS: {has_crs}")
    
    # Testar extração de CRS
    print("\n2. Extraindo CRS do arquivo...")
    crs = handler._extract_crs_from_netcdf(test_file)
    print(f"   CRS extraído: {crs}")
    
    # Testar correção se necessário
    if not has_crs:
        print("\n3. Arquivo não tem CRS, testando correção...")
        fixed_file = handler._fix_netcdf_crs(test_file)
        print(f"   Arquivo corrigido: {fixed_file}")
        
        if fixed_file != test_file and os.path.exists(fixed_file):
            print("   ✅ Correção bem-sucedida!")
            
            # Verificar se o arquivo corrigido tem CRS
            has_crs_fixed = handler._has_crs_info(fixed_file)
            print(f"   Arquivo corrigido tem CRS: {has_crs_fixed}")
            
            # Limpar arquivo temporário
            os.unlink(fixed_file)
        else:
            print("   ❌ Correção falhou")
    else:
        print("\n3. Arquivo já tem CRS, correção não necessária")
    
    # Testar extract_resource_to_publish
    print("\n4. Testando extract_resource_to_publish...")
    files = {"base_file": test_file}
    resources = handler.extract_resource_to_publish(
        files=files,
        action="upload",
        layer_name="test_layer",
        alternate="test_alternate"
    )
    
    print(f"   Recursos extraídos: {len(resources)}")
    for i, resource in enumerate(resources):
        print(f"   Recurso {i+1}:")
        print(f"     Nome: {resource.get('name')}")
        print(f"     CRS: {resource.get('crs')}")
        print(f"     Caminho: {resource.get('raster_path')}")
    
    print("\n✅ Teste concluído!")
    return True

if __name__ == "__main__":
    test_netcdf_crs_fix()
