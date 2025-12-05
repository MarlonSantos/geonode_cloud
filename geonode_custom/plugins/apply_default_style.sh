#!/bin/bash

# Script para aplicar o estilo sst_colormap como padrão para camadas raster
# Este script deve ser executado após o GeoServer estar rodando

echo "=== Aplicando estilo padrão para camadas raster ==="

# Configurações do GeoServer
GEOSERVER_URL="http://localhost:8080/geoserver"
ADMIN_USER="admin"
ADMIN_PASSWORD="geoserver"
DEFAULT_STYLE="sst_colormap"

# Aguardar GeoServer estar disponível (com timeout de 5 minutos)
echo "=== Aguardando GeoServer estar disponível (timeout: 5 minutos) ==="
timeout=300
elapsed=0
while [ $elapsed -lt $timeout ]; do
    if curl -s -o /dev/null -w "%{http_code}" "$GEOSERVER_URL/rest/about/status" | grep -q "200"; then
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

# Função para aplicar estilo padrão a uma camada
apply_default_style() {
    local layer_name=$1
    local workspace=$2
    
    echo "=== Aplicando estilo padrão à camada: $layer_name ==="
    
    # Construir URL da camada
    if [ -n "$workspace" ]; then
        layer_url="$GEOSERVER_URL/rest/layers/$workspace:$layer_name"
    else
        layer_url="$GEOSERVER_URL/rest/layers/$layer_name"
    fi
    
    # Verificar se a camada existe
    layer_response=$(curl -s -u "$ADMIN_USER:$ADMIN_PASSWORD" "$layer_url")
    if echo "$layer_response" | grep -q "404"; then
        echo "   Camada $layer_name não encontrada, pulando..."
        return
    fi
    
    # Verificar se é uma camada raster
    if echo "$layer_response" | grep -q '"type":"RASTER"'; then
        echo "   Camada $layer_name é raster, aplicando estilo padrão..."
        
        # Aplicar o estilo padrão
        curl -u "$ADMIN_USER:$ADMIN_PASSWORD" \
             -X PUT \
             -H "Content-type: application/json" \
             -d "{\"layer\":{\"defaultStyle\":{\"name\":\"$DEFAULT_STYLE\"}}}" \
             "$layer_url"
        
        if [ $? -eq 0 ]; then
            echo "   ✓ Estilo padrão aplicado com sucesso à camada $layer_name"
        else
            echo "   ✗ Erro ao aplicar estilo padrão à camada $layer_name"
        fi
    else
        echo "   Camada $layer_name não é raster, pulando..."
    fi
}

# Função para listar e processar todas as camadas
process_all_layers() {
    echo "=== Listando todas as camadas ==="
    
    # Obter lista de camadas
    layers_response=$(curl -s -u "$ADMIN_USER:$ADMIN_PASSWORD" "$GEOSERVER_URL/rest/layers")
    
    # Extrair nomes das camadas
    layer_names=$(echo "$layers_response" | grep -o '<name>[^<]*</name>' | sed 's/<name>\(.*\)<\/name>/\1/')
    
    echo "Camadas encontradas:"
    echo "$layer_names" | while read layer_name; do
        if [ -n "$layer_name" ]; then
            echo "  - $layer_name"
            apply_default_style "$layer_name"
        fi
    done
}

# Função para processar camadas por workspace
process_workspace_layers() {
    local workspace=$1
    
    echo "=== Processando camadas do workspace: $workspace ==="
    
    # Obter lista de camadas do workspace
    workspace_layers_response=$(curl -s -u "$ADMIN_USER:$ADMIN_PASSWORD" "$GEOSERVER_URL/rest/workspaces/$workspace/layers")
    
    # Extrair nomes das camadas
    layer_names=$(echo "$workspace_layers_response" | grep -o '<name>[^<]*</name>' | sed 's/<name>\(.*\)<\/name>/\1/')
    
    echo "Camadas encontradas no workspace $workspace:"
    echo "$layer_names" | while read layer_name; do
        if [ -n "$layer_name" ]; then
            echo "  - $layer_name"
            apply_default_style "$layer_name" "$workspace"
        fi
    done
}

# Função para configurar estilo padrão global
set_global_default_style() {
    echo "=== Configurando estilo padrão global ==="
    
    # Verificar se o estilo existe
    style_response=$(curl -s -u "$ADMIN_USER:$ADMIN_PASSWORD" "$GEOSERVER_URL/rest/styles/$DEFAULT_STYLE")
    if echo "$style_response" | grep -q "404"; then
        echo "   Estilo $DEFAULT_STYLE não encontrado, criando primeiro..."
        return 1
    fi
    
    echo "   Estilo $DEFAULT_STYLE encontrado"
    return 0
}

# Executar o processo
echo "=== Iniciando aplicação de estilo padrão ==="

# Primeiro, verificar se o estilo padrão existe
if set_global_default_style; then
    # Processar todas as camadas
    process_all_layers
    
    # Processar camadas por workspace (opcional)
    # Descomente as linhas abaixo se quiser processar workspaces específicos
    # process_workspace_layers "geonode"
    # process_workspace_layers "outro_workspace"
    
    echo ""
    echo "=== Aplicação de estilo padrão concluída ==="
    echo "✓ O estilo $DEFAULT_STYLE foi aplicado como padrão para todas as camadas raster"
    echo ""
    echo "Para verificar:"
    echo "1. Acesse o GeoServer: $GEOSERVER_URL"
    echo "2. Vá para Layers"
    echo "3. Verifique se as camadas raster têm o estilo $DEFAULT_STYLE como padrão"
else
    echo "   Erro: Estilo $DEFAULT_STYLE não está disponível"
    exit 1
fi
