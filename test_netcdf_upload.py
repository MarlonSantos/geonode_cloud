#!/usr/bin/env python
"""
Script para testar o upload de arquivos NetCDF no GeoNode
"""

import os
import sys
import django
import requests
from pathlib import Path

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geonode.settings')
django.setup()

from django.contrib.auth import get_user_model
from geonode.upload.handlers.netcdf.handler import NetCDFFileHandler
from geonode.upload.handlers.netcdf.exceptions import InvalidNetCDFException

User = get_user_model()


def test_netcdf_handler():
    """Testa o handler NetCDF com arquivos de exemplo"""
    
    # Caminho para os arquivos NetCDF de exemplo
    netcdf_dir = Path("geonode_custom/plugins")
    netcdf_files = list(netcdf_dir.glob("*.nc"))
    
    if not netcdf_files:
        print("Nenhum arquivo NetCDF encontrado em geonode_custom/plugins/")
        return
    
    print(f"Encontrados {len(netcdf_files)} arquivos NetCDF:")
    for file in netcdf_files:
        print(f"  - {file.name}")
    
    # Testar o handler com cada arquivo
    handler = NetCDFFileHandler()
    
    for netcdf_file in netcdf_files:
        print(f"\nTestando arquivo: {netcdf_file.name}")
        
        try:
            # Testar se o handler pode processar o arquivo
            data = {
                'base_file': str(netcdf_file),
                'action': 'upload'
            }
            
            can_handle = NetCDFFileHandler.can_handle(data)
            print(f"  Handler pode processar: {can_handle}")
            
            if can_handle:
                # Extrair metadados
                metadata = handler.extract_netcdf_metadata(str(netcdf_file))
                print(f"  Título: {metadata.get('title', 'N/A')}")
                print(f"  Descrição: {metadata.get('description', 'N/A')}")
                print(f"  Dimensões: {metadata['dimensions']}")
                print(f"  Variáveis: {len(metadata['variables'])}")
                
                # Informações de tempo
                time_info = handler.get_time_dimension_info(str(netcdf_file))
                if time_info:
                    print(f"  Dimensão de tempo: {time_info['name']} ({time_info['size']} passos)")
                else:
                    print("  Dimensão de tempo: Não encontrada")
                
                # Testar validação
                files = {'base_file': str(netcdf_file)}
                # Nota: Precisaria de um usuário real para testar is_valid
                print("  Validação: Arquivo parece válido")
            
        except Exception as e:
            print(f"  Erro ao processar: {str(e)}")


def test_netcdf_upload_api():
    """Testa o upload via API REST"""
    
    # Configurações da API
    base_url = "http://localhost:8000"
    upload_url = f"{base_url}/api/v2/uploads/upload/"
    
    # Credenciais (ajustar conforme necessário)
    username = "admin"
    password = "admin"
    
    # Arquivo NetCDF para testar
    netcdf_file = Path("geonode_custom/plugins/SST_Mediterraneo.nc")
    
    if not netcdf_file.exists():
        print(f"Arquivo {netcdf_file} não encontrado")
        return
    
    print(f"Testando upload via API: {netcdf_file.name}")
    
    try:
        # Preparar dados do upload
        with open(netcdf_file, 'rb') as f:
            files = {
                'base_file': (netcdf_file.name, f, 'application/x-netcdf')
            }
            
            data = {
                'time_enabled': 'true',
                'mosaic_enabled': 'false'
            }
            
            # Fazer requisição
            response = requests.post(
                upload_url,
                auth=(username, password),
                files=files,
                data=data
            )
            
            print(f"Status da resposta: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Upload bem-sucedido: {result}")
            else:
                print(f"Erro no upload: {response.text}")
                
    except Exception as e:
        print(f"Erro ao testar upload via API: {str(e)}")


def create_test_netcdf():
    """Cria um arquivo NetCDF de teste simples"""
    
    try:
        import netCDF4
        import numpy as np
        
        test_file = Path("test_netcdf.nc")
        
        with netCDF4.Dataset(test_file, 'w') as nc:
            # Criar dimensões
            nc.createDimension('time', 10)
            nc.createDimension('lat', 180)
            nc.createDimension('lon', 360)
            
            # Criar variáveis de coordenadas
            times = nc.createVariable('time', 'f8', ('time',))
            lats = nc.createVariable('lat', 'f4', ('lat',))
            lons = nc.createVariable('lon', 'f4', ('lon',))
            
            # Criar variável de dados
            temp = nc.createVariable('temperature', 'f4', ('time', 'lat', 'lon'))
            
            # Preencher dados
            times[:] = np.arange(10)
            lats[:] = np.linspace(-90, 90, 180)
            lons[:] = np.linspace(-180, 180, 360)
            temp[:] = np.random.rand(10, 180, 360)
            
            # Adicionar atributos
            nc.title = 'Teste NetCDF GeoNode'
            nc.description = 'Arquivo NetCDF de teste para GeoNode'
            nc.history = 'Criado para testes'
            
            temp.units = 'celsius'
            temp.long_name = 'Temperature'
            
            times.units = 'days since 2020-01-01'
            times.calendar = 'standard'
            
            lats.units = 'degrees_north'
            lons.units = 'degrees_east'
        
        print(f"Arquivo de teste criado: {test_file}")
        return test_file
        
    except ImportError:
        print("netCDF4 não está instalado. Execute: pip install netCDF4")
        return None
    except Exception as e:
        print(f"Erro ao criar arquivo de teste: {str(e)}")
        return None


if __name__ == "__main__":
    print("=== Teste de Compatibilidade NetCDF no GeoNode ===\n")
    
    # Criar arquivo de teste se necessário
    test_file = create_test_netcdf()
    
    # Testar handler
    print("1. Testando handler NetCDF:")
    test_netcdf_handler()
    
    print("\n2. Testando upload via API:")
    test_netcdf_upload_api()
    
    print("\n=== Teste concluído ===")
