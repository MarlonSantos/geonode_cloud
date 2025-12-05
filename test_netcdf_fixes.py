#!/usr/bin/env python
"""
Script para testar as correções do NetCDF após rebuild
"""

import os
import sys
import requests
import time

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geonode.settings')

import django
django.setup()

from geonode.upload.handlers.netcdf.handler import NetCDFFileHandler

def test_netcdf_variables_discovery():
    """Testa a descoberta de variáveis NetCDF"""
    print("=== Testando descoberta de variáveis NetCDF ===")
    
    # Arquivo de teste
    test_file = "simple_global_example.nc"
    if not os.path.exists(test_file):
        print(f"❌ Arquivo de teste não encontrado: {test_file}")
        return False
    
    try:
        variables = NetCDFFileHandler._get_netcdf_variables_static(test_file)
        print(f"✅ Variáveis encontradas: {variables}")
        
        if variables:
            print("✅ Descoberta de variáveis funcionando")
            return True
        else:
            print("❌ Nenhuma variável encontrada")
            return False
            
    except Exception as e:
        print(f"❌ Erro na descoberta de variáveis: {e}")
        return False

def test_geoserver_wms():
    """Testa se o WMS está funcionando"""
    print("\n=== Testando WMS do GeoServer ===")
    
    try:
        response = requests.get(
            "http://localhost/geoserver/wms?service=WMS&version=1.1.1&request=GetCapabilities",
            timeout=10
        )
        
        if response.status_code == 200:
            if "ServiceException" not in response.text:
                print("✅ WMS GetCapabilities funcionando")
                return True
            else:
                print("❌ WMS retornando erro de serviço")
                print(f"Erro: {response.text[:200]}...")
                return False
        else:
            print(f"❌ WMS retornando status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar WMS: {e}")
        return False

def test_geoserver_layers():
    """Testa se há layers disponíveis"""
    print("\n=== Testando layers do GeoServer ===")
    
    try:
        response = requests.get(
            "http://localhost/geoserver/rest/layers",
            auth=('admin', 'geoserver'),
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            layers = data.get('layers', {}).get('layer', [])
            
            if layers:
                print(f"✅ {len(layers)} layers encontrados")
                for layer in layers[:5]:  # Mostrar apenas os primeiros 5
                    print(f"  - {layer.get('name', 'N/A')}")
                return True
            else:
                print("❌ Nenhum layer encontrado")
                return False
        else:
            print(f"❌ Erro ao listar layers: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar layers: {e}")
        return False

def test_netcdf_coverage_stores():
    """Testa se há coverage stores NetCDF"""
    print("\n=== Testando coverage stores NetCDF ===")
    
    try:
        response = requests.get(
            "http://localhost/geoserver/rest/workspaces/geonode/coveragestores",
            auth=('admin', 'geoserver'),
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            stores = data.get('coverageStores', {}).get('coverageStore', [])
            
            netcdf_stores = [store for store in stores if 'netcdf' in store.get('name', '').lower()]
            
            if netcdf_stores:
                print(f"✅ {len(netcdf_stores)} coverage stores NetCDF encontrados")
                for store in netcdf_stores:
                    print(f"  - {store.get('name', 'N/A')}")
                return True
            else:
                print("❌ Nenhum coverage store NetCDF encontrado")
                return False
        else:
            print(f"❌ Erro ao listar coverage stores: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar coverage stores: {e}")
        return False

def main():
    """Função principal"""
    print("🧪 TESTE DAS CORREÇÕES NETCDF")
    print("=" * 50)
    
    # Aguardar GeoServer ficar pronto
    print("⏳ Aguardando GeoServer ficar pronto...")
    time.sleep(5)
    
    # Executar testes
    tests = [
        test_netcdf_variables_discovery,
        test_geoserver_wms,
        test_geoserver_layers,
        test_netcdf_coverage_stores
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erro no teste {test.__name__}: {e}")
            results.append(False)
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Testes aprovados: {passed}/{total}")
    print(f"❌ Testes falharam: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 TODAS AS CORREÇÕES FUNCIONANDO!")
        print("✅ NetCDF está pronto para uso")
    else:
        print("\n⚠️  ALGUMAS CORREÇÕES PRECISAM DE AJUSTE")
        print("❌ Verifique os logs para mais detalhes")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


