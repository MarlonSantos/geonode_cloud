#!/bin/bash

# Script para registrar estilos SLD no GeoServer via REST API
# Este script deve ser executado após o GeoServer estar rodando

echo "=== Aguardando GeoServer estar disponível ==="

# Aguardar GeoServer estar disponível (com timeout de 5 minutos)
echo "=== Aguardando GeoServer estar disponível (timeout: 5 minutos) ==="
timeout=300
elapsed=0
while [ $elapsed -lt $timeout ]; do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/geoserver/rest/about/status | grep -q "200"; then
        break
    fi
    echo "GeoServer ainda não está disponível, aguardando... ($elapsed/$timeout segundos)"
    sleep 10
    elapsed=$((elapsed + 10))
done

if [ $elapsed -ge $timeout ]; then
    echo "Timeout: GeoServer não ficou disponível em $timeout segundos"
    exit 1
fi

echo "=== GeoServer está disponível ==="

# Configurações do GeoServer
GEOSERVER_URL="http://localhost:8080/geoserver"
ADMIN_USER="admin"
ADMIN_PASSWORD="geoserver"

# Função para registrar um estilo
register_style() {
    local style_name=$1
    local sld_file=$2
    
    echo "=== Registrando estilo: $style_name ==="
    
    # Verificar se o estilo já existe
    if curl -s -u "$ADMIN_USER:$ADMIN_PASSWORD" "$GEOSERVER_URL/rest/styles/$style_name" | grep -q "404"; then
        echo "Estilo $style_name não existe, criando..."
        
        # Criar o estilo
        curl -u "$ADMIN_USER:$ADMIN_PASSWORD" \
             -X POST \
             -H "Content-type: application/vnd.ogc.sld+xml" \
             -d @"$sld_file" \
             "$GEOSERVER_URL/rest/styles"
        
        if [ $? -eq 0 ]; then
            echo "Estilo $style_name criado com sucesso"
        else
            echo "Erro ao criar estilo $style_name"
        fi
    else
        echo "Estilo $style_name já existe, atualizando..."
        
        # Atualizar o estilo existente
        curl -u "$ADMIN_USER:$ADMIN_PASSWORD" \
             -X PUT \
             -H "Content-type: application/vnd.ogc.sld+xml" \
             -d @"$sld_file" \
             "$GEOSERVER_URL/rest/styles/$style_name"
        
        if [ $? -eq 0 ]; then
            echo "Estilo $style_name atualizado com sucesso"
        else
            echo "Erro ao atualizar estilo $style_name"
        fi
    fi
}

# Registrar o estilo SST colormap
if [ -f "/geoserver_data/data/styles/sst_colormap.sld" ]; then
    register_style "sst_colormap" "/geoserver_data/data/styles/sst_colormap.sld"
    
    # Aguardar um pouco para garantir que o estilo foi registrado
    echo "=== Aguardando estilo ser registrado ==="
    sleep 5
    
    # Aplicar o estilo como padrão para camadas raster
    echo "=== Aplicando estilo como padrão para camadas raster ==="
    /usr/local/bin/apply_default_style.sh
    
else
    echo "Arquivo sst_colormap.sld não encontrado em /geoserver_data/data/styles/"
fi

echo "=== Registro de estilos concluído ==="
