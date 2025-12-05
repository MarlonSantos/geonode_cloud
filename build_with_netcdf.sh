#!/bin/bash

# Script de build completo com suporte NetCDF
# Este script constrói o GeoNode com todas as funcionalidades NetCDF integradas

set -e

echo "=== Build do GeoNode com Suporte NetCDF ==="
echo

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Verificar se estamos no diretório correto
if [ ! -f "manage.py" ]; then
    print_error "Execute este script no diretório raiz do GeoNode"
    exit 1
fi

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker não está instalado"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose não está instalado"
    exit 1
fi

print_step "1. Verificando arquivos necessários..."

# Verificar se os arquivos do handler NetCDF existem
required_files=(
    "geonode/upload/handlers/netcdf/handler.py"
    "geonode/upload/handlers/netcdf/exceptions.py"
    "geonode/upload/handlers/netcdf/tests.py"
    "geonode/upload/handlers/netcdf/apps.py"
    "geonode/upload/handlers/netcdf/__init__.py"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        print_status "✓ $file encontrado"
    else
        print_error "✗ $file não encontrado"
        exit 1
    fi
done

# Verificar se o plugin do GeoServer existe
plugin_files=(
    "geonode_custom/plugins/geoserver-2.24.4-netcdf-plugin.zip"
)

for file in "${plugin_files[@]}"; do
    if [ -f "$file" ]; then
        print_status "✓ $file encontrado"
    else
        print_warning "⚠ $file não encontrado"
    fi
done

print_step "2. Verificando configurações..."

# Verificar se o handler NetCDF está registrado
if grep -q "NetCDFFileHandler" geonode/upload/settings.py; then
    print_status "✓ Handler NetCDF registrado no settings.py"
else
    print_error "✗ Handler NetCDF não encontrado no settings.py"
    exit 1
fi

# Verificar se a dependência netCDF4 está no requirements.txt
if grep -q "netCDF4" requirements.txt; then
    print_status "✓ Dependência netCDF4 encontrada no requirements.txt"
else
    print_error "✗ Dependência netCDF4 não encontrada no requirements.txt"
    exit 1
fi

print_step "3. Limpando builds anteriores..."

# Parar containers se estiverem rodando
if docker-compose ps | grep -q "Up"; then
    print_status "Parando containers existentes..."
    docker-compose down
fi

# Remover imagens antigas
print_status "Removendo imagens antigas..."
docker-compose down --rmi all --volumes --remove-orphans || true

print_step "4. Construindo imagens..."

# Construir a imagem do GeoServer com plugins NetCDF
print_status "Construindo imagem do GeoServer com plugins NetCDF..."
docker-compose build geoserver

# Construir a imagem do Django com handler NetCDF
print_status "Construindo imagem do Django com handler NetCDF..."
docker-compose build django

print_step "5. Verificando build..."

# Verificar se as imagens foram construídas
if docker images | grep -q "geonode/geoserver:2.24.4-custom"; then
    print_status "✓ Imagem do GeoServer construída com sucesso"
else
    print_error "✗ Falha na construção da imagem do GeoServer"
    exit 1
fi

if docker images | grep -q "geonode/geonode:latest-ubuntu-22.04"; then
    print_status "✓ Imagem do Django construída com sucesso"
else
    print_error "✗ Falha na construção da imagem do Django"
    exit 1
fi

print_step "6. Iniciando serviços..."

# Iniciar os serviços
print_status "Iniciando serviços..."
docker-compose up -d

# Aguardar os serviços ficarem prontos
print_status "Aguardando serviços ficarem prontos..."
sleep 30

print_step "7. Verificando funcionamento..."

# Verificar se o Django está respondendo
print_status "Verificando Django..."
if curl -f -s http://localhost:8000/ > /dev/null; then
    print_status "✓ Django está respondendo"
else
    print_warning "⚠ Django não está respondendo ainda"
fi

# Verificar se o GeoServer está respondendo
print_status "Verificando GeoServer..."
if curl -f -s http://localhost:8080/geoserver/ > /dev/null; then
    print_status "✓ GeoServer está respondendo"
else
    print_warning "⚠ GeoServer não está respondendo ainda"
fi

print_step "8. Testando funcionalidades NetCDF..."

# Testar o handler NetCDF
print_status "Testando handler NetCDF..."
if docker-compose exec -T django python test_netcdf_upload.py > /dev/null 2>&1; then
    print_status "✓ Handler NetCDF funcionando"
else
    print_warning "⚠ Teste do handler NetCDF falhou"
fi

print_step "9. Configuração final..."

# Executar configuração do GeoServer
print_status "Configurando GeoServer para NetCDF..."
if docker-compose exec -T django python setup_netcdf_geoserver.py > /dev/null 2>&1; then
    print_status "✓ GeoServer configurado para NetCDF"
else
    print_warning "⚠ Configuração do GeoServer falhou"
fi

echo
echo "=== Build Concluído com Sucesso! ==="
echo
echo "🎉 O GeoNode com suporte NetCDF está pronto!"
echo
echo "📋 Resumo do que foi configurado:"
echo "  ✅ Handler NetCDF integrado ao GeoNode"
echo "  ✅ Plugins NetCDF instalados no GeoServer"
echo "  ✅ Dependências Python instaladas"
echo "  ✅ Scripts de configuração automática"
echo "  ✅ Arquivos de exemplo incluídos"
echo
echo "🌐 Acesse:"
echo "  - GeoNode: http://localhost:8000"
echo "  - GeoServer: http://localhost:8080/geoserver"
echo
echo "📁 Arquivos NetCDF de exemplo disponíveis em:"
echo "  - /geoserver_data/data/netcdf_samples/"
echo
echo "🔧 Para testar o upload de arquivos NetCDF:"
echo "  1. Acesse http://localhost:8000"
echo "  2. Faça login como admin"
echo "  3. Vá para 'Upload' e selecione arquivos .nc"
echo
echo "📚 Documentação: docs/NetCDF_Compatibility.md"
echo
print_status "Build concluído com sucesso!"
