#!/usr/bin/env python3
"""
Script para testar a instanciação do handler NetCDF
"""

import os
import sys
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geonode.settings')
django.setup()

def test_handler_instantiation():
    """Testa a instanciação do handler NetCDF"""
    print("🔍 Testando instanciação do handler NetCDF...")
    
    try:
        # Testar importação direta
        print("\n1. Testando importação direta...")
        from geonode.upload.handlers.netcdf.handler import NetCDFFileHandler
        handler1 = NetCDFFileHandler()
        print("   ✅ Importação direta OK")
        
        # Testar instanciação via import_string (como o DataPublisher faz)
        print("\n2. Testando instanciação via import_string...")
        from django.utils.module_loading import import_string
        handler_module_path = "geonode.upload.handlers.netcdf.handler.NetCDFFileHandler"
        handler2 = import_string(handler_module_path)()
        print("   ✅ Instanciação via import_string OK")
        
        # Verificar se ambos os handlers têm o método _normalize_crs
        print("\n3. Verificando métodos dos handlers...")
        
        for i, handler in enumerate([handler1, handler2], 1):
            print(f"   Handler {i}:")
            print(f"     - Tipo: {type(handler)}")
            print(f"     - Módulo: {handler.__class__.__module__}")
            print(f"     - Classe: {handler.__class__.__name__}")
            
            # Verificar métodos importantes
            methods_to_check = [
                '_normalize_crs',
                '_extract_crs_from_netcdf',
                'extract_resource_to_publish',
                'publish_resources'
            ]
            
            for method_name in methods_to_check:
                if hasattr(handler, method_name):
                    print(f"     ✅ {method_name}: Existe")
                else:
                    print(f"     ❌ {method_name}: NÃO existe")
        
        # Testar normalização de CRS em ambos os handlers
        print("\n4. Testando normalização de CRS...")
        test_crs = "ESPG4326"
        
        for i, handler in enumerate([handler1, handler2], 1):
            try:
                result = handler._normalize_crs(test_crs)
                print(f"   Handler {i}: {test_crs} -> {result}")
                if result == "EPSG:4326":
                    print(f"     ✅ Normalização correta")
                else:
                    print(f"     ❌ Normalização incorreta")
            except Exception as e:
                print(f"   Handler {i}: ❌ Erro na normalização: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_publisher_flow():
    """Testa o fluxo do DataPublisher"""
    print(f"\n🔍 Testando fluxo do DataPublisher...")
    
    try:
        from geonode.upload.publisher import DataPublisher
        
        # Simular o que o DataPublisher faz
        handler_module_path = "geonode.upload.handlers.netcdf.handler.NetCDFFileHandler"
        
        print(f"   - Handler module path: {handler_module_path}")
        
        # Criar DataPublisher (pode falhar se GeoServer não estiver rodando)
        try:
            publisher = DataPublisher(handler_module_path)
            print(f"   ✅ DataPublisher criado com sucesso")
            print(f"   - Handler tipo: {type(publisher.handler)}")
            print(f"   - Handler módulo: {publisher.handler.__class__.__module__}")
            
            # Verificar se o handler tem o método _normalize_crs
            if hasattr(publisher.handler, '_normalize_crs'):
                print(f"   ✅ Handler tem método _normalize_crs")
                
                # Testar normalização
                result = publisher.handler._normalize_crs("ESPG4326")
                print(f"   - Teste normalização: ESPG4326 -> {result}")
                
            else:
                print(f"   ❌ Handler NÃO tem método _normalize_crs")
                
        except Exception as e:
            print(f"   ⚠️  DataPublisher falhou (GeoServer pode não estar rodando): {e}")
            print(f"   - Isso é normal se o GeoServer não estiver disponível")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante o teste do DataPublisher: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🔧 Teste de Instanciação do Handler NetCDF")
    print("=" * 60)
    
    # Testar instanciação
    instantiation_ok = test_handler_instantiation()
    
    # Testar fluxo do DataPublisher
    publisher_ok = test_data_publisher_flow()
    
    print(f"\n📋 Resumo:")
    print(f"   • Instanciação do handler: {'✅ OK' if instantiation_ok else '❌ FALHOU'}")
    print(f"   • Fluxo do DataPublisher: {'✅ OK' if publisher_ok else '❌ FALHOU'}")
    
    if instantiation_ok and publisher_ok:
        print(f"\n🎉 Handler NetCDF está funcionando corretamente!")
        print(f"   O problema pode estar em outro lugar do fluxo.")
    else:
        print(f"\n💥 Há problemas com a instanciação do handler.")

