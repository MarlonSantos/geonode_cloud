#!/bin/bash

# Script para copiar arquivos NetCDF para o volume do GeoServer
# Este script pode ser executado manualmente dentro do container se necessário

echo "=== Copiando arquivos NetCDF para o volume ==="

# Verificar se o diretório temporário existe
if [ ! -d "/tmp/netcdf_samples" ]; then
    echo "ERRO: Diretório /tmp/netcdf_samples não encontrado!"
    exit 1
fi

# Criar diretório de destino
mkdir -p /geoserver_data/data/netcdf_samples/

# Copiar arquivos
cp -r /tmp/netcdf_samples/* /geoserver_data/data/netcdf_samples/

# Verificar se a cópia foi bem-sucedida
if [ $? -eq 0 ]; then
    echo "=== Arquivos NetCDF copiados com sucesso para /geoserver_data/data/netcdf_samples/ ==="
    ls -la /geoserver_data/data/netcdf_samples/
else
    echo "ERRO: Falha ao copiar arquivos NetCDF!"
    exit 1
fi
