#!/usr/bin/env python3
"""
Script para criar arquivo NetCDF de exemplo com dados mundiais
Dados de temperatura global com padrão bem evidente para visualização
"""

import netCDF4
import numpy as np
import os

def create_global_temperature_netcdf():
    """Criar arquivo NetCDF com dados de temperatura global"""
    
    # Arquivo de saída
    output_file = 'global_temperature_example.nc'
    
    # Dimensões globais (resolução 2 graus para arquivo menor)
    lats = np.arange(-90, 91, 2)  # -90 a 90 graus, passo 2
    lons = np.arange(-180, 181, 2)  # -180 a 180 graus, passo 2
    
    print(f"Criando dados para {len(lats)} latitudes x {len(lons)} longitudes")
    
    # Criar grid de coordenadas
    lat_grid, lon_grid = np.meshgrid(lats, lons, indexing='ij')
    
    # Simular temperatura global com padrão bem evidente
    # 1. Gradiente latitudinal (quente no equador, frio nos polos)
    temperature = 30 - 50 * np.abs(lat_grid) / 90
    
    # 2. Adicionar padrão continental (variação longitudinal)
    temperature += 15 * np.sin(lon_grid * np.pi / 180) * np.cos(lat_grid * np.pi / 180)
    
    # 3. Adicionar "continentes" (regiões mais quentes)
    # América do Norte
    mask_na = (lat_grid >= 30) & (lat_grid <= 70) & (lon_grid >= -140) & (lon_grid <= -60)
    temperature[mask_na] += 5
    
    # Europa
    mask_eu = (lat_grid >= 40) & (lat_grid <= 70) & (lon_grid >= -10) & (lon_grid <= 40)
    temperature[mask_eu] += 5
    
    # Ásia
    mask_asia = (lat_grid >= 20) & (lat_grid <= 60) & (lon_grid >= 60) & (lon_grid <= 140)
    temperature[mask_asia] += 5
    
    # 4. Adicionar ruído mínimo para realismo
    temperature += np.random.normal(0, 1, temperature.shape)
    
    # Criar arquivo NetCDF
    with netCDF4.Dataset(output_file, 'w', format='NETCDF4') as nc:
        # Criar dimensões
        nc.createDimension('lat', len(lats))
        nc.createDimension('lon', len(lons))
        
        # Criar variáveis de coordenadas
        lat_var = nc.createVariable('lat', 'f4', ('lat',))
        lon_var = nc.createVariable('lon', 'f4', ('lon',))
        
        lat_var[:] = lats
        lon_var[:] = lons
        
        lat_var.units = 'degrees_north'
        lat_var.long_name = 'latitude'
        lat_var.standard_name = 'latitude'
        
        lon_var.units = 'degrees_east'
        lon_var.long_name = 'longitude'
        lon_var.standard_name = 'longitude'
        
        # Criar variável de temperatura
        temp_var = nc.createVariable('temperature', 'f4', ('lat', 'lon'))
        temp_var[:] = temperature
        temp_var.units = 'Celsius'
        temp_var.long_name = 'Global Surface Temperature'
        temp_var.standard_name = 'air_temperature'
        temp_var.missing_value = -999.0
        temp_var.valid_range = [-50.0, 50.0]
        
        # Atributos globais
        nc.title = 'Global Temperature Example Dataset'
        nc.description = 'Simulated global surface temperature data for NetCDF visualization testing'
        nc.history = 'Created for NetCDF visualization testing in GeoNode'
        nc.source = 'Simulated data - temperature pattern with continental effects'
        nc.Conventions = 'CF-1.6'
        nc.institution = 'GeoNode NetCDF Testing'
        nc.references = 'Generated for visualization testing'
    
    print(f"\n✅ Arquivo criado: {output_file}")
    print(f"📊 Tamanho: {os.path.getsize(output_file):,} bytes")
    print(f"🌍 Dimensões: {len(lats)} x {len(lons)} = {len(lats) * len(lons):,} pontos")
    print(f"🌡️  Temperatura range: {temperature.min():.1f}°C a {temperature.max():.1f}°C")
    print(f"📈 Padrão: Quente no equador, frio nos polos + efeitos continentais")
    
    return output_file

def create_simple_global_netcdf():
    """Criar arquivo NetCDF mais simples com padrão bem evidente"""
    
    output_file = 'simple_global_example.nc'
    
    # Dimensões menores para teste rápido
    lats = np.arange(-90, 91, 5)  # 37 pontos
    lons = np.arange(-180, 181, 5)  # 73 pontos
    
    print(f"Criando arquivo simples: {len(lats)} x {len(lons)} = {len(lats) * len(lons)} pontos")
    
    # Grid
    lat_grid, lon_grid = np.meshgrid(lats, lons, indexing='ij')
    
    # Padrão muito simples e evidente
    # Gradiente latitudinal puro
    temperature = 40 - 80 * np.abs(lat_grid) / 90
    
    # Adicionar faixas longitudinais para tornar mais evidente
    temperature += 20 * np.sin(lon_grid * np.pi / 90)
    
    with netCDF4.Dataset(output_file, 'w', format='NETCDF4') as nc:
        nc.createDimension('lat', len(lats))
        nc.createDimension('lon', len(lons))
        
        lat_var = nc.createVariable('lat', 'f4', ('lat',))
        lon_var = nc.createVariable('lon', 'f4', ('lon',))
        temp_var = nc.createVariable('temperature', 'f4', ('lat', 'lon'))
        
        lat_var[:] = lats
        lon_var[:] = lons
        temp_var[:] = temperature
        
        lat_var.units = 'degrees_north'
        lon_var.units = 'degrees_east'
        temp_var.units = 'Celsius'
        temp_var.long_name = 'Global Temperature'
        
        nc.title = 'Simple Global Temperature Example'
        nc.description = 'Very simple global temperature pattern for testing'
        nc.Conventions = 'CF-1.6'
    
    print(f"\n✅ Arquivo simples criado: {output_file}")
    print(f"📊 Tamanho: {os.path.getsize(output_file):,} bytes")
    print(f"🌡️  Temperatura range: {temperature.min():.1f}°C a {temperature.max():.1f}°C")
    
    return output_file

if __name__ == "__main__":
    print("🌍 Criando arquivos NetCDF de exemplo para visualização...")
    print("=" * 60)
    
    # Criar arquivo completo
    print("\n1. Criando arquivo completo com padrão realista:")
    create_global_temperature_netcdf()
    
    print("\n" + "=" * 60)
    
    # Criar arquivo simples
    print("\n2. Criando arquivo simples com padrão evidente:")
    create_simple_global_netcdf()
    
    print("\n" + "=" * 60)
    print("🎯 Arquivos prontos para upload no GeoNode!")
    print("📁 Use qualquer um dos arquivos .nc criados")
    print("🌡️  Padrão esperado: Gradiente latitudinal + variações longitudinais")


