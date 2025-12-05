#!/bin/bash

# Script para corrigir arquivos NetCDF que não têm informações de CRS/SRID
# Uso: ./correct_netcdf_files.sh [arquivo_netcdf]

echo "=== Corretor de CRS para Arquivos NetCDF ==="

# Verificar se nco está instalado
if ! command -v ncap2 &> /dev/null; then
    echo "Instalando NCO (NetCDF Operators)..."
    apt-get update && apt-get install -y nco
fi

# Função para corrigir um arquivo NetCDF
fix_netcdf_crs() {
    local input_file="$1"
    local output_file="${input_file%.nc}_fixed.nc"
    local temp_file="${input_file%.nc}_temp.nc"
    
    echo "Corrigindo CRS do arquivo: $input_file"
    
    # Verificar se o arquivo existe
    if [ ! -f "$input_file" ]; then
        echo "❌ Arquivo não encontrado: $input_file"
        return 1
    fi
    
    # Adicionar variável CRS
    echo "  - Adicionando variável CRS..."
    if ! ncap2 -s 'crs=0' "$input_file" "$temp_file"; then
        echo "❌ Erro ao adicionar variável CRS"
        return 1
    fi
    
    # Adicionar atributos CRS básicos
    echo "  - Adicionando atributos CRS..."
    if ! ncatted -O -a 'grid_mapping_name,crs,c,c,latitude_longitude' "$temp_file" "$output_file"; then
        echo "❌ Erro ao adicionar atributos CRS"
        rm -f "$temp_file"
        return 1
    fi
    
    # Adicionar grid_mapping à variável de dados
    echo "  - Adicionando grid_mapping..."
    if ! ncatted -O -a 'grid_mapping,delta_sst_mean,c,c,crs' "$output_file"; then
        echo "⚠️  Aviso: Não foi possível adicionar grid_mapping (variável pode ter nome diferente)"
    fi
    
    # Limpar arquivo temporário
    rm -f "$temp_file"
    
    echo "✅ Arquivo corrigido: $output_file"
    return 0
}

# Se um arquivo foi especificado, corrigir apenas esse arquivo
if [ $# -eq 1 ]; then
    fix_netcdf_crs "$1"
    exit $?
fi

# Caso contrário, corrigir todos os arquivos NetCDF no diretório atual
echo "Procurando arquivos NetCDF para corrigir..."
find . -name "*.nc" -type f | while read -r file; do
    echo ""
    fix_netcdf_crs "$file"
done

echo ""
echo "=== Correção concluída ==="
echo "Arquivos corrigidos têm sufixo '_fixed.nc'"
echo "Use os arquivos corrigidos para upload no GeoNode"
