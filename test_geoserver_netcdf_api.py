#!/usr/bin/env python3
"""
Script para testar a API REST do GeoServer para NetCDF
"""

import os
import sys
import django
import tempfile
import netCDF4
import numpy as np
import requests

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geonode.settings')
django.setup()

from django.conf import settings
from geonode.geoserver.helpers import ogc_server_settings

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
        nc.title = 'Test NetCDF for GeoServer API'
        nc.description = 'A test NetCDF file for testing GeoServer API'
        nc.epsg = 4326
    
    return temp_file.name

def test_geoserver_netcdf_api():
    """Testa a API REST do GeoServer para NetCDF"""
    print("🌐 Testando API REST do GeoServer para NetCDF...")
    
    # Verificar se o GeoServer está rodando
    try:
        username, password = ogc_server_settings.credentials
        geoserver_url = ogc_server_settings.rest
        
        print(f"✓ GeoServer URL: {geoserver_url}")
        print(f"✓ Usuário: {username}")
        
        # Testar conexão básica
        response = requests.get(
            f"{geoserver_url}/about/status.json",
            auth=(username, password),
            timeout=10
        )
        
        if response.status_code == 200:
            print("✓ Conexão com GeoServer estabelecida")
        else:
            print(f"❌ Falha na conexão: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao conectar com GeoServer: {str(e)}")
        return False
    
    # Criar arquivo de teste
    test_file = create_test_netcdf()
    print(f"✓ Arquivo de teste criado: {test_file}")
    
    try:
        workspace_name = "geonode"
        store_name = "test_netcdf_store"
        
        # 1. Verificar se o workspace existe
        print(f"\n1. Verificando workspace '{workspace_name}'...")
        response = requests.get(
            f"{geoserver_url}/workspaces/{workspace_name}.json",
            auth=(username, password)
        )
        
        if response.status_code == 200:
            print(f"✓ Workspace '{workspace_name}' existe")
        else:
            print(f"⚠️  Workspace '{workspace_name}' não existe ou erro: {response.status_code}")
        
        # 2. Criar coverage store NetCDF
        print(f"\n2. Criando coverage store NetCDF '{store_name}'...")
        store_data = {
            "coverageStore": {
                "name": store_name,
                "type": "NetCDF",
                "enabled": True,
                "description": f"Test NetCDF coverage store",
                "workspace": {
                    "name": workspace_name
                }
            }
        }
        
        response = requests.post(
            f"{geoserver_url}/workspaces/{workspace_name}/coveragestores",
            auth=(username, password),
            json=store_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code in [200, 201]:
            print(f"✓ Coverage store '{store_name}' criado com sucesso")
        else:
            print(f"❌ Falha ao criar coverage store: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
        
        # 3. Upload do arquivo NetCDF
        print(f"\n3. Fazendo upload do arquivo NetCDF...")
        with open(test_file, 'rb') as f:
            upload_response = requests.put(
                f"{geoserver_url}/workspaces/{workspace_name}/coveragestores/{store_name}/file.netcdf",
                auth=(username, password),
                data=f,
                headers={'Content-Type': 'application/netcdf'}
            )
        
        if upload_response.status_code in [200, 201]:
            print(f"✓ Arquivo NetCDF enviado com sucesso")
        else:
            print(f"❌ Falha no upload: {upload_response.status_code}")
            print(f"   Resposta: {upload_response.text}")
            return False
        
        # 4. Verificar se a camada foi criada
        print(f"\n4. Verificando se a camada foi criada...")
        response = requests.get(
            f"{geoserver_url}/workspaces/{workspace_name}/coveragestores/{store_name}/coverages.json",
            auth=(username, password)
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'coverages' in data and 'coverage' in data['coverages']:
                coverages = data['coverages']['coverage']
                if isinstance(coverages, list):
                    print(f"✓ {len(coverages)} camada(s) criada(s)")
                    for coverage in coverages:
                        print(f"   - {coverage.get('name', 'N/A')}")
                else:
                    print(f"✓ 1 camada criada: {coverages.get('name', 'N/A')}")
            else:
                print("⚠️  Nenhuma camada encontrada")
        else:
            print(f"❌ Erro ao verificar camadas: {response.status_code}")
        
        print("\n✅ Teste da API REST do GeoServer para NetCDF concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Limpar arquivo de teste
        os.unlink(test_file)
        print(f"\n✓ Arquivo de teste removido: {test_file}")

if __name__ == '__main__':
    success = test_geoserver_netcdf_api()
    if success:
        print("\n🎉 Todos os testes passaram! A API REST do GeoServer está funcionando para NetCDF.")
    else:
        print("\n💥 Alguns testes falharam. Verifique os logs acima.")

