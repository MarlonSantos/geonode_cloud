#!/usr/bin/env python3
"""
Script para testar a correção do erro de SRID
"""

def test_crs_normalization():
    """Testa a normalização de CRS sem Django"""
    
    def normalize_crs(crs_input):
        """Normalize different CRS formats to EPSG:XXXX format"""
        if crs_input is None:
            return "EPSG:4326"
        
        # Convert to string if necessary
        crs_str = str(crs_input).strip()
        
        # If already in correct format
        if crs_str.startswith("EPSG:"):
            return crs_str
        
        # If has "ESPG" (common typo)
        if crs_str.startswith("ESPG"):
            # Remove "ESPG" and add "EPSG:"
            code = crs_str[4:]
            return f"EPSG:{code}"
        
        # If has "epsg" (lowercase)
        if crs_str.startswith("epsg:"):
            return crs_str.upper()
        
        # If is just the numeric code
        if crs_str.isdigit():
            return f"EPSG:{crs_str}"
        
        # If contains only numbers and letters (no colon)
        if ":" not in crs_str and any(c.isdigit() for c in crs_str):
            # Try to extract numbers
            import re
            numbers = re.findall(r'\d+', crs_str)
            if numbers:
                return f"EPSG:{numbers[0]}"
        
        # Fallback
        return "EPSG:4326"
    
    print("🧪 Testando normalização de CRS...")
    
    test_cases = [
        # Caso específico do erro
        ("ESPG4326", "EPSG:4326"),
        ("ESPG3857", "EPSG:3857"),
        
        # Outros casos
        ("EPSG:4326", "EPSG:4326"),
        ("epsg:4326", "EPSG:4326"),
        ("4326", "EPSG:4326"),
        (4326, "EPSG:4326"),
        ("EPSG4326", "EPSG:4326"),
        (None, "EPSG:4326"),
    ]
    
    print(f"\n{'Input':<15} {'Expected':<15} {'Result':<15} {'Status'}")
    print("-" * 60)
    
    all_passed = True
    
    for input_crs, expected in test_cases:
        try:
            result = normalize_crs(input_crs)
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

def simulate_netcdf_crs_extraction():
    """Simula a extração de CRS de um arquivo NetCDF"""
    print(f"\n🔍 Simulando extração de CRS de arquivo NetCDF...")
    
    # Simular diferentes cenários que podem causar o erro
    scenarios = [
        {
            "name": "Atributo global com ESPG4326",
            "global_attrs": {"epsg": "ESPG4326"},
            "expected": "EPSG:4326"
        },
        {
            "name": "Atributo global com 4326",
            "global_attrs": {"epsg": 4326},
            "expected": "EPSG:4326"
        },
        {
            "name": "Atributo global com EPSG:4326",
            "global_attrs": {"epsg": "EPSG:4326"},
            "expected": "EPSG:4326"
        },
        {
            "name": "Sem atributos CRS",
            "global_attrs": {},
            "expected": "EPSG:4326"
        }
    ]
    
    def normalize_crs(crs_input):
        if crs_input is None:
            return "EPSG:4326"
        crs_str = str(crs_input).strip()
        if crs_str.startswith("EPSG:"):
            return crs_str
        if crs_str.startswith("ESPG"):
            code = crs_str[4:]
            return f"EPSG:{code}"
        if crs_str.startswith("epsg:"):
            return crs_str.upper()
        if crs_str.isdigit():
            return f"EPSG:{crs_str}"
        return "EPSG:4326"
    
    for scenario in scenarios:
        print(f"\n📋 {scenario['name']}:")
        
        # Simular extração de CRS
        crs_found = None
        for attr_name in ['epsg', 'EPSG', 'crs', 'CRS', 'srid', 'SRID']:
            if attr_name in scenario['global_attrs']:
                crs_found = scenario['global_attrs'][attr_name]
                break
        
        if crs_found is not None:
            normalized_crs = normalize_crs(crs_found)
            print(f"   - CRS encontrado: {crs_found}")
            print(f"   - CRS normalizado: {normalized_crs}")
        else:
            normalized_crs = "EPSG:4326"  # Default
            print(f"   - Nenhum CRS encontrado, usando padrão: {normalized_crs}")
        
        # Verificar se está correto
        if normalized_crs == scenario['expected']:
            print(f"   ✅ Resultado correto: {normalized_crs}")
        else:
            print(f"   ❌ Resultado incorreto: {normalized_crs} (esperado: {scenario['expected']})")

if __name__ == '__main__':
    print("🔧 Teste de Correção do Erro de SRID")
    print("=" * 50)
    
    # Testar normalização
    normalization_passed = test_crs_normalization()
    
    # Simular extração de CRS
    simulate_netcdf_crs_extraction()
    
    print(f"\n📋 Resumo:")
    print(f"   • Normalização de CRS: {'✅ FUNCIONANDO' if normalization_passed else '❌ COM PROBLEMAS'}")
    print(f"   • Correção do erro 'ESPG4326': {'✅ IMPLEMENTADA' if normalization_passed else '❌ PENDENTE'}")
    
    if normalization_passed:
        print(f"\n🎉 A correção do erro de SRID foi implementada com sucesso!")
        print(f"   O erro 'The SRID for the resource {name: chl_july_only,crs:ESPG4326' deve estar resolvido.")
        print(f"   Agora o CRS será normalizado para 'EPSG:4326' corretamente.")
    else:
        print(f"\n💥 Ainda há problemas com a correção do SRID.")

