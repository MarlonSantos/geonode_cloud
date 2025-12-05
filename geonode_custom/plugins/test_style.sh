#!/bin/bash

# Script de teste para verificar se o estilo SST colormap foi registrado corretamente

echo "=== Teste do Estilo SST Colormap ==="

# Configurações do GeoServer
GEOSERVER_URL="http://localhost:8080/geoserver"
ADMIN_USER="admin"
ADMIN_PASSWORD="geoserver"

# Teste 1: Verificar se o GeoServer está respondendo
echo "1. Testando conectividade com GeoServer..."
response=$(curl -s -o /dev/null -w "%{http_code}" "$GEOSERVER_URL/rest/about/status")
if [ "$response" = "200" ]; then
    echo "   ✓ GeoServer está respondendo"
else
    echo "   ✗ GeoServer não está respondendo (código: $response)"
    exit 1
fi

# Teste 2: Verificar se o estilo existe
echo "2. Verificando se o estilo 'sst_colormap' existe..."
style_response=$(curl -s -u "$ADMIN_USER:$ADMIN_PASSWORD" "$GEOSERVER_URL/rest/styles/sst_colormap")
if echo "$style_response" | grep -q "sst_colormap"; then
    echo "   ✓ Estilo 'sst_colormap' encontrado"
else
    echo "   ✗ Estilo 'sst_colormap' não encontrado"
    echo "   Resposta: $style_response"
    exit 1
fi

# Teste 3: Verificar se o arquivo SLD está no volume
echo "3. Verificando se o arquivo SLD está no volume..."
if [ -f "/geoserver_data/data/styles/sst_colormap.sld" ]; then
    echo "   ✓ Arquivo sst_colormap.sld encontrado no volume"
    echo "   Tamanho: $(ls -lh /geoserver_data/data/styles/sst_colormap.sld | awk '{print $5}')"
else
    echo "   ✗ Arquivo sst_colormap.sld não encontrado no volume"
    exit 1
fi

# Teste 4: Verificar conteúdo do SLD
echo "4. Verificando conteúdo do arquivo SLD..."
if grep -q "sst_colormap" /geoserver_data/data/styles/sst_colormap.sld; then
    echo "   ✓ Arquivo SLD contém o nome correto"
else
    echo "   ✗ Arquivo SLD não contém o nome correto"
    exit 1
fi

if grep -q "ColorMap" /geoserver_data/data/styles/sst_colormap.sld; then
    echo "   ✓ Arquivo SLD contém definição de ColorMap"
else
    echo "   ✗ Arquivo SLD não contém definição de ColorMap"
    exit 1
fi

# Teste 5: Listar todos os estilos disponíveis
echo "5. Listando todos os estilos disponíveis..."
styles_list=$(curl -s -u "$ADMIN_USER:$ADMIN_PASSWORD" "$GEOSERVER_URL/rest/styles" | grep -o '<name>[^<]*</name>' | sed 's/<name>\(.*\)<\/name>/\1/')
echo "   Estilos encontrados:"
echo "$styles_list" | while read style; do
    if [ "$style" = "sst_colormap" ]; then
        echo "   ✓ $style (nosso estilo)"
    else
        echo "   - $style"
    fi
done

echo ""
echo "=== Teste Concluído ==="
echo "✓ Todos os testes passaram! O estilo SST colormap foi registrado com sucesso."
echo ""
echo "Para usar o estilo:"
echo "1. Acesse o GeoServer: $GEOSERVER_URL"
echo "2. Vá para Layers > [sua camada raster] > Edit"
echo "3. Selecione 'sst_colormap' na lista de estilos"
echo "4. Salve as alterações"
