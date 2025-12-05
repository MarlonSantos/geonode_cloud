#!/usr/bin/env python3
"""
Script para corrigir arquivos NetCDF que não têm informações de CRS/SRID
"""

import os
import sys
import subprocess
import tempfile
import shutil

def fix_netcdf_crs(input_file, output_file=None):
    """
    Corrige um arquivo NetCDF adicionando informações de CRS (EPSG:4326)
    """
    if output_file is None:
        output_file = input_file.replace('.nc', '_fixed.nc')
    
    print(f"Corrigindo CRS do arquivo: {input_file}")
    print(f"Arquivo de saída: {output_file}")
    
    try:
        # Criar arquivo temporário com variável CRS
        temp_file = input_file.replace('.nc', '_temp.nc')
        
        # Adicionar variável CRS
        cmd1 = ['ncap2', '-s', 'crs=0', input_file, temp_file]
        result1 = subprocess.run(cmd1, capture_output=True, text=True)
        if result1.returncode != 0:
            print(f"Erro ao adicionar variável CRS: {result1.stderr}")
            return False
        
        # Adicionar atributos CRS
        cmd2 = [
            'ncatted', '-O',
            '-a', 'grid_mapping_name,crs,c,c,latitude_longitude',
            '-a', 'longitude_of_prime_meridian,crs,c,d,0.0',
            '-a', 'semi_major_axis,crs,c,d,6378137.0',
            '-a', 'inverse_flattening,crs,c,d,298.257223563',
            '-a', 'spatial_ref,crs,c,c,GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]',
            temp_file, output_file
        ]
        result2 = subprocess.run(cmd2, capture_output=True, text=True)
        if result2.returncode != 0:
            print(f"Erro ao adicionar atributos CRS: {result2.stderr}")
            return False
        
        # Adicionar grid_mapping à variável de dados
        # Primeiro, precisamos identificar a variável de dados
        cmd3 = ['ncdump', '-h', output_file]
        result3 = subprocess.run(cmd3, capture_output=True, text=True)
        if result3.returncode != 0:
            print(f"Erro ao ler cabeçalho: {result3.stderr}")
            return False
        
        # Encontrar variáveis que não são coordenadas
        lines = result3.stdout.split('\n')
        data_vars = []
        for line in lines:
            if 'float' in line and '(' in line and ')' in line:
                var_name = line.split()[1].split('(')[0]
                if var_name not in ['lat', 'lon', 'latitude', 'longitude', 'crs']:
                    data_vars.append(var_name)
        
        # Adicionar grid_mapping a todas as variáveis de dados
        for var in data_vars:
            cmd4 = ['ncatted', '-O', '-a', f'grid_mapping,{var},c,c,crs', output_file]
            result4 = subprocess.run(cmd4, capture_output=True, text=True)
            if result4.returncode != 0:
                print(f"Erro ao adicionar grid_mapping para {var}: {result4.stderr}")
                return False
        
        # Limpar arquivo temporário
        os.remove(temp_file)
        
        print(f"✅ Arquivo corrigido com sucesso: {output_file}")
        return True
        
    except Exception as e:
        print(f"Erro durante a correção: {str(e)}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Uso: python fix_netcdf_crs.py <arquivo_netcdf> [arquivo_saida]")
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

if __name__ == "__main__":
    main()
