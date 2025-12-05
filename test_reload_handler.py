#!/usr/bin/env python3
"""
Script para testar o reload do handler NetCDF
"""

import os
import sys
import django
import importlib

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geonode.settings')
django.setup()

def test_handler_reload():
    """Testa o reload do handler NetCDF"""
    print("🔍 Testando reload do handler NetCDF...")
    
    try:
        # Importar o módulo
        from geonode.upload.handlers import netcdf
        print("   ✅ Módulo netcdf importado")
        
        # Verificar se tem o handler
        if hasattr(netcdf, 'handler'):
            print("   ✅ Módulo tem handler")
            
            # Recarregar o módulo
            importlib.reload(netcdf.handler)
            print("   ✅ Módulo handler recarregado")
            
            # Importar a classe
            from geonode.upload.handlers.netcdf.handler import NetCDFFileHandler
            print("   ✅ Classe NetCDFFileHandler importada")
            
            # Instanciar
            handler = NetCDFFileHandler()
            print("   ✅ Handler instanciado")
            
            # Verificar se tem o método _normalize_crs
            if hasattr(handler, '_normalize_crs'):
                print("   ✅ Handler tem método _normalize_crs")
                
                # Testar o método
                result = handler._normalize_crs("ESPG4326")
                print(f"   - Teste: ESPG4326 -> {result}")
                
                if result == "EPSG:4326":
                    print("   ✅ Normalização funcionando corretamente")
                    return True
                else:
                    print("   ❌ Normalização não está funcionando")
                    return False
            else:
                print("   ❌ Handler NÃO tem método _normalize_crs")
                return False
        else:
            print("   ❌ Módulo não tem handler")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_import():
    """Testa importação direta sem Django"""
    print(f"\n🔍 Testando importação direta...")
    
    try:
        # Adicionar o path do projeto
        sys.path.insert(0, os.getcwd())
        
        # Importar diretamente
        from geonode.upload.handlers.netcdf.handler import NetCDFFileHandler
        print("   ✅ Importação direta OK")
        
        # Instanciar
        handler = NetCDFFileHandler()
        print("   ✅ Instanciação OK")
        
        # Verificar método
        if hasattr(handler, '_normalize_crs'):
            print("   ✅ Método _normalize_crs existe")
            
            # Testar
            result = handler._normalize_crs("ESPG4326")
            print(f"   - Teste: ESPG4326 -> {result}")
            
            if result == "EPSG:4326":
                print("   ✅ Normalização funcionando")
                return True
            else:
                print("   ❌ Normalização não funcionando")
                return False
        else:
            print("   ❌ Método _normalize_crs não existe")
            return False
            
    except Exception as e:
        print(f"❌ Erro na importação direta: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("🔧 Teste de Reload do Handler NetCDF")
    print("=" * 50)
    
    # Testar reload
    reload_ok = test_handler_reload()
    
    # Testar importação direta
    direct_ok = test_direct_import()
    
    print(f"\n📋 Resumo:")
    print(f"   • Reload do handler: {'✅ OK' if reload_ok else '❌ FALHOU'}")
    print(f"   • Importação direta: {'✅ OK' if direct_ok else '❌ FALHOU'}")
    
    if reload_ok and direct_ok:
        print(f"\n🎉 Handler NetCDF está funcionando corretamente!")
        print(f"   O problema pode estar em outro lugar do fluxo.")
    else:
        print(f"\n💥 Há problemas com o handler NetCDF.")

