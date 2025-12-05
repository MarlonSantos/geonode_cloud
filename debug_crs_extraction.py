#!/usr/bin/env python3
"""
Script para debugar a extração de CRS de arquivos NetCDF
"""

import os
import sys
import django
import netCDF4

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geonode.settings')
django.setup()

from geonode.upload.handlers.netcdf.handler import NetCDFFileHandler

def debug_crs_extraction(file_path):
    """Debuga a extração de CRS de um arquivo NetCDF específico"""
    print(f"🔍 Debugando extração de CRS do arquivo: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ Arquivo não encontrado: {file_path}")
        return
    
    try:
        # 1. Verificar se é um arquivo NetCDF válido
        print(f"\n1. Verificando se é um arquivo NetCDF válido...")
        with netCDF4.Dataset(file_path, 'r') as nc:
            print(f"   ✓ Arquivo NetCDF válido")
            print(f"   - Dimensões: {list(nc.dimensions.keys())}")
            print(f"   - Variáveis: {list(nc.variables.keys())}")
            
            # 2. Verificar atributos globais
            print(f"\n2. Verificando atributos globais...")
            global_attrs = nc.ncattrs()
            print(f"   - Atributos globais: {global_attrs}")
            
            for attr in global_attrs:
                value = getattr(nc, attr)
                print(f"   - {attr}: {value} (tipo: {type(value)})")
            
            # 3. Verificar variáveis com grid_mapping
            print(f"\n3. Verificando variáveis com grid_mapping...")
            for var_name, var in nc.variables.items():
                if hasattr(var, 'grid_mapping'):
                    print(f"   - {var_name} tem grid_mapping: {var.grid_mapping}")
                    if var.grid_mapping in nc.variables:
                        grid_var = nc.variables[var.grid_mapping]
                        print(f"     - Variável {var.grid_mapping} encontrada")
                        grid_attrs = grid_var.ncattrs()
                        print(f"     - Atributos: {grid_attrs}")
                        for attr in grid_attrs:
                            value = getattr(grid_var, attr)
                            print(f"       - {attr}: {value} (tipo: {type(value)})")
            
            # 4. Testar extração de CRS usando o handler
            print(f"\n4. Testando extração de CRS usando o handler...")
            handler = NetCDFFileHandler()
            crs = handler._extract_crs_from_netcdf(file_path)
            print(f"   - CRS extraído: '{crs}' (tipo: {type(crs)})")
            print(f"   - Tamanho da string: {len(crs)}")
            print(f"   - Caracteres: {[ord(c) for c in crs]}")
            
            # 5. Verificar se o CRS está no formato correto
            print(f"\n5. Verificando formato do CRS...")
            if crs.startswith("EPSG:"):
                print(f"   ✅ Formato correto: {crs}")
            else:
                print(f"   ❌ Formato incorreto: {crs}")
                print(f"   - Esperado: EPSG:XXXX")
                print(f"   - Recebido: {crs}")
            
            # 6. Testar com pyproj se disponível
            print(f"\n6. Testando com pyproj...")
            try:
                from pyproj import CRS
                if crs.startswith("EPSG:"):
                    epsg_code = crs.split(":")[1]
                    test_crs = CRS.from_epsg(int(epsg_code))
                    print(f"   ✅ CRS válido: {test_crs}")
                else:
                    print(f"   ❌ Não é possível testar CRS inválido: {crs}")
            except ImportError:
                print(f"   ⚠️  pyproj não disponível")
            except Exception as e:
                print(f"   ❌ Erro ao testar CRS: {e}")
                
    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {e}")
        import traceback
        traceback.print_exc()

def test_crs_formats():
    """Testa diferentes formatos de CRS"""
    print(f"\n🧪 Testando diferentes formatos de CRS...")
    
    test_cases = [
        "EPSG:4326",
        "ESPG4326",  # Erro comum
        "epsg:4326",
        "4326",
        4326,
        "EPSG4326",
        "EPSG:4326 ",
        " EPSG:4326",
    ]
    
    for test_crs in test_cases:
        print(f"   - Testando: '{test_crs}' (tipo: {type(test_crs)})")
        
        # Normalizar CRS
        normalized = normalize_crs(test_crs)
        print(f"     → Normalizado: '{normalized}'")
        
        # Verificar se é válido
        if normalized.startswith("EPSG:"):
            print(f"     ✅ Válido")
        else:
            print(f"     ❌ Inválido")

def normalize_crs(crs_input):
    """Normaliza diferentes formatos de CRS para EPSG:XXXX"""
    if crs_input is None:
        return "EPSG:4326"
    
    # Converter para string se necessário
    crs_str = str(crs_input).strip()
    
    # Se já está no formato correto
    if crs_str.startswith("EPSG:"):
        return crs_str
    
    # Se tem "ESPG" (erro comum)
    if crs_str.startswith("ESPG"):
        # Remover "ESPG" e adicionar "EPSG:"
        code = crs_str[4:]
        return f"EPSG:{code}"
    
    # Se tem "epsg" (minúsculo)
    if crs_str.startswith("epsg:"):
        return crs_str.upper()
    
    # Se é apenas o código numérico
    if crs_str.isdigit():
        return f"EPSG:{crs_str}"
    
    # Se contém apenas números e letras (sem dois pontos)
    if ":" not in crs_str and any(c.isdigit() for c in crs_str):
        # Tentar extrair números
        import re
        numbers = re.findall(r'\d+', crs_str)
        if numbers:
            return f"EPSG:{numbers[0]}"
    
    # Fallback
    return "EPSG:4326"

if __name__ == '__main__':
    print("🔍 Debug de Extração de CRS de Arquivos NetCDF")
    print("=" * 60)
    
    # Testar formatos de CRS
    test_crs_formats()
    
    # Se um arquivo foi especificado, debugar
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        debug_crs_extraction(file_path)
    else:
        print(f"\n💡 Para debugar um arquivo específico, execute:")
        print(f"   python debug_crs_extraction.py /caminho/para/arquivo.nc")

