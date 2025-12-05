#!/bin/bash

# Script para monitorar novas camadas raster e aplicar o estilo padrão automaticamente
# Este script roda em background e verifica periodicamente por novas camadas

echo "=== Iniciando monitoramento de novas camadas raster ==="

# Configurações do GeoServer
GEOSERVER_URL="http://localhost:8080/geoserver"
ADMIN_USER="admin"
ADMIN_PASSWORD="geoserver"
DEFAULT_STYLE="sst_colormap"
CHECK_INTERVAL=60  # Verificar a cada 60 segundos

# Função para obter lista de camadas
get_layers_list() {
    curl -s -u "$ADMIN_USER:$ADMIN_PASSWORD" "$GEOSERVER_URL/rest/layers" | \
    grep -o '<name>[^<]*</name>' | sed 's/<name>\(.*\)<\/name>/\1/'
}

# Função para aplicar estilo padrão a uma camada raster
apply_style_to_raster_layer() {
    local layer_name=$1
    
    # Verificar se é uma camada raster
    layer_info=$(curl -s -u "$ADMIN_USER:$ADMIN_PASSWORD" "$GEOSERVER_URL/rest/layers/$layer_name")
    
    if echo "$layer_info" | grep -q '"type":"RASTER"'; then
        echo "   Aplicando estilo padrão à nova camada raster: $layer_name"
        
        # Aplicar o estilo padrão
        curl -u "$ADMIN_USER:$ADMIN_PASSWORD" \
             -X PUT \
             -H "Content-type: application/json" \
             -d "{\"layer\":{\"defaultStyle\":{\"name\":\"$DEFAULT_STYLE\"}}}" \
             "$GEOSERVER_URL/rest/layers/$layer_name"
        
        if [ $? -eq 0 ]; then
            echo "   ✓ Estilo padrão aplicado com sucesso à camada $layer_name"
        else
            echo "   ✗ Erro ao aplicar estilo padrão à camada $layer_name"
        fi
    fi
}

# Função principal de monitoramento
monitor_layers() {
    echo "=== Monitoramento ativo - verificando a cada $CHECK_INTERVAL segundos ==="
    
    # Obter lista inicial de camadas
    previous_layers=$(get_layers_list)
    echo "Camadas iniciais:"
    echo "$previous_layers" | while read layer; do
        if [ -n "$layer" ]; then
            echo "  - $layer"
        fi
    done
    
    # Loop de monitoramento
    while true; do
        sleep $CHECK_INTERVAL
        
        # Obter lista atual de camadas
        current_layers=$(get_layers_list)
        
        # Comparar listas para encontrar novas camadas
        new_layers=""
        while read layer; do
            if [ -n "$layer" ]; then
                if ! echo "$previous_layers" | grep -q "^$layer$"; then
                    new_layers="$new_layers$layer"$'\n'
                fi
            fi
        done <<< "$current_layers"
        
        # Processar novas camadas
        if [ -n "$new_layers" ]; then
            echo "=== Novas camadas detectadas: ==="
            echo "$new_layers" | while read layer; do
                if [ -n "$layer" ]; then
                    echo "  - $layer"
                    apply_style_to_raster_layer "$layer"
                fi
            done
        fi
        
        # Atualizar lista anterior
        previous_layers="$current_layers"
    done
}

# Verificar se o GeoServer está disponível
echo "=== Verificando conectividade com GeoServer ==="
if curl -s -o /dev/null -w "%{http_code}" "$GEOSERVER_URL/rest/about/status" | grep -q "200"; then
    echo "✓ GeoServer está disponível"
else
    echo "✗ GeoServer não está disponível"
    exit 1
fi

# Verificar se o estilo padrão existe
echo "=== Verificando se o estilo padrão existe ==="
if curl -s -u "$ADMIN_USER:$ADMIN_PASSWORD" "$GEOSERVER_URL/rest/styles/$DEFAULT_STYLE" | grep -q "404"; then
    echo "✗ Estilo $DEFAULT_STYLE não encontrado"
    exit 1
else
    echo "✓ Estilo $DEFAULT_STYLE encontrado"
fi

# Iniciar monitoramento
monitor_layers
