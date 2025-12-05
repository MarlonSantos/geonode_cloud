#!/usr/bin/env python3
"""
Script para testar a normalização de CRS
"""

import os
import sys
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geonode.settings')
django.setup()

from geonode.upload.handlers.netcdf.handler import NetCDFFileHandler

def test_crs_normalization():
    """Testa a normalização de diferentes formatos de CRS"""
    print("🧪 Testando normalização de CRS...")
    
    handler = NetCDFFileHandler()
    
    test_cases = [
        # Formato correto
        ("EPSG:4326", "EPSG:4326"),
        ("EPSG:3857", "EPSG:3857"),
        
        # Erro comum: ESPG em vez de EPSG
        ("ESPG4326", "EPSG:4326"),
        ("ESPG3857", "EPSG:3857"),
        
        # Minúsculo
        ("epsg:4326", "EPSG:4326"),
        ("epsg:3857", "EPSG:3857"),
        
        # Apenas o código numérico
        ("4326", "EPSG:4326"),
        ("3857", "EPSG:3857"),
        (4326, "EPSG:4326"),
        (3857, "EPSG:3857"),
        
        # Sem dois pontos
        ("EPSG4326", "EPSG:4326"),
        ("EPSG3857", "EPSG:3857"),
        
        # Com espaços
        (" EPSG:4326 ", "EPSG:4326"),
        (" EPSG4326 ", "EPSG:4326"),
        
        # Casos especiais
        (None, "EPSG:4326"),
        ("", "EPSG:4326"),
        ("invalid", "EPSG:4326"),
    ]
    
    print(f"\n{'Input':<15} {'Expected':<15} {'Result':<15} {'Status'}")
    print("-" * 60)
    
    all_passed = True
    
    for input_crs, expected in test_cases:
        try:
            result = handler._normalize_crs(input_crs)
            status = "✅ PASS" if result == expected else "❌ FAIL"
            if result != expected:
                all_passed = False
            
            print(f"{str(input_crs):<15} {expected:<15} {result:<15} {status}")
        except Exception as e:
            print(f"{str(input_crs):<15} {expected:<15} {'ERROR':<15} ❌ FAIL ({e})")
            all_passed = False
    
    print("-" * 60)
    if all_passed:
        print("🎉 Todos os testes passaram!")
    else:
        print("💥 Alguns testes falharam!")
    
    return all_passed

def test_specific_crs_issue():
    """Testa o caso específico do erro reportado"""
    print(f"\n🔍 Testando caso específico do erro...")
    
    handler = NetCDFFileHandler()
    
    # Simular o caso que está causando o erro
    problematic_crs = "ESPG4326"  # Erro comum: falta o ":" e tem "ESPG" em vez de "EPSG"
    
    print(f"CRS problemático: '{problematic_crs}'")
    normalized = handler._normalize_crs(problematic_crs)
    print(f"CRS normalizado: '{normalized}'")
    
    if normalized == "EPSG:4326":
        print("✅ Problema corrigido!")
        return True
    else:
        print("❌ Problema ainda existe!")
        return False

if __name__ == '__main__':
    print("🔧 Teste de Normalização de CRS")
    print("=" * 50)
    
    # Testar normalização geral
    general_test_passed = test_crs_normalization()
    
    # Testar caso específico
    specific_test_passed = test_specific_crs_issue()
    
    print(f"\n📋 Resumo:")
    print(f"   • Teste geral: {'✅ PASSOU' if general_test_passed else '❌ FALHOU'}")
    print(f"   • Teste específico: {'✅ PASSOU' if specific_test_passed else '❌ FALHOU'}")
    
    if general_test_passed and specific_test_passed:
        print(f"\n🎉 Correção do CRS implementada com sucesso!")
        print(f"   O erro 'ESPG4326' agora será corrigido para 'EPSG:4326'")
    else:
        print(f"\n💥 Ainda há problemas com a normalização de CRS")

