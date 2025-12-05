#!/usr/bin/env python3
"""
Script simples para corrigir arquivos NetCDF que não têm informações de CRS/SRID
"""

import subprocess
import os
import sys

def fix_netcdf_crs(input_file, output_file=None):
    """
    Corrige um arquivo NetCDF adicionando informações de CRS (EPSG:4326)
    """
    if output_file is None:
        output_file = input_file.replace('.nc', '_fixed.nc')
    
    print(f"Corrigindo CRS do arquivo: {input_file}")
    print(f"Arquivo de saída: {output_file}")
    
    temp_file = input_file.replace('.nc', '_temp.nc')
    
    try:
        # Adicionar variável CRS
        cmd1 = ['ncap2', '-s', 'crs=0', input_file, temp_file]
        result1 = subprocess.run(cmd1, capture_output=True, text=True)
        if result1.returncode != 0:
            print(f"Erro ao adicionar variável CRS: {result1.stderr}")
            return False
        
        # Adicionar atributos CRS básicos
        cmd2 = ['ncatted', '-O', '-a', 'grid_mapping_name,crs,c,c,latitude_longitude', temp_file, output_file]
        result2 = subprocess.run(cmd2, capture_output=True, text=True)
        if result2.returncode != 0:
            print(f"Erro ao adicionar atributos CRS: {result2.stderr}")
            return False
        
        # Adicionar grid_mapping à variável de dados
        # Para este arquivo específico, sabemos que a variável é delta_sst_mean
        cmd3 = ['ncatted', '-O', '-a', 'grid_mapping,delta_sst_mean,c,c,crs', output_file]
        result3 = subprocess.run(cmd3, capture_output=True, text=True)
        if result3.returncode != 0:
            print(f"Erro ao adicionar grid_mapping: {result3.stderr}")
            return False
        
        # Limpar arquivo temporário
        if os.path.exists(temp_file):
            os.remove(temp_file)
        
        print(f"✅ Arquivo corrigido com sucesso: {output_file}")
        return True
        
    except Exception as e:
        print(f"Erro durante a correção: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python fix_netcdf_crs_simple.py <arquivo_netcdf> [arquivo_saida]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"Arquivo não encontrado: {input_file}")
        sys.exit(1)
    
    success = fix_netcdf_crs(input_file, output_file)
    if success:
        print("Correção concluída com sucesso!")
    else:
        print("Falha na correção do arquivo.")
        sys.exit(1)
