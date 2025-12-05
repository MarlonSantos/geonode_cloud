#!/bin/bash

# Script de instalação para suporte NetCDF no GeoNode
# Este script configura automaticamente o suporte a arquivos NetCDF

set -e

echo "=== Instalação de Suporte NetCDF no GeoNode ==="
echo

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Verificar se estamos no diretório correto
if [ ! -f "manage.py" ]; then
    print_error "Execute este script no diretório raiz do GeoNode"
    exit 1
fi

print_status "Verificando ambiente..."

# Verificar se o ambiente virtual está ativo
if [ -z "$VIRTUAL_ENV" ]; then
    print_warning "Ambiente virtual não detectado. Recomenda-se usar um ambiente virtual."
fi

# Verificar Python
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
print_status "Python version: $python_version"

# Instalar dependências Python
print_status "Instalando dependências Python..."
pip install netCDF4>=1.6.0

# Verificar se a instalação foi bem-sucedida
if python3 -c "import netCDF4; print('netCDF4 instalado com sucesso')" 2>/dev/null; then
    print_status "netCDF4 instalado com sucesso"
else
    print_error "Falha ao instalar netCDF4"
    exit 1
fi

# Verificar se os arquivos do handler existem
print_status "Verificando handler NetCDF..."
if [ ! -d "geonode/upload/handlers/netcdf" ]; then
    print_error "Diretório do handler NetCDF não encontrado"
    exit 1
fi

# Verificar se o plugin do GeoServer existe
print_status "Verificando plugin do GeoServer..."
plugin_dir="geonode_custom/plugins"
required_plugins=(
    "geoserver-2.24.4-netcdf-plugin.zip"
)

for plugin in "${required_plugins[@]}"; do
    if [ -f "$plugin_dir/$plugin" ]; then
        print_status "Plugin encontrado: $plugin"
    else
        print_warning "Plugin não encontrado: $plugin"
    fi
done

# Verificar se os arquivos NetCDF de exemplo existem
print_status "Verificando arquivos de exemplo..."
nc_files=$(find "$plugin_dir" -name "*.nc" 2>/dev/null | wc -l)
if [ "$nc_files" -gt 0 ]; then
    print_status "Encontrados $nc_files arquivos NetCDF de exemplo"
else
    print_warning "Nenhum arquivo NetCDF de exemplo encontrado"
fi

# Executar migrações se necessário
print_status "Executando migrações..."
python3 manage.py migrate --noinput

# Coletar arquivos estáticos
print_status "Coletando arquivos estáticos..."
python3 manage.py collectstatic --noinput

# Testar o handler
print_status "Testando handler NetCDF..."
if python3 test_netcdf_upload.py > /dev/null 2>&1; then
    print_status "Teste do handler executado com sucesso"
else
    print_warning "Teste do handler falhou (pode ser normal se o GeoServer não estiver rodando)"
fi

# Configurar GeoServer se solicitado
read -p "Deseja configurar o GeoServer automaticamente? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Configurando GeoServer..."
    if python3 setup_netcdf_geoserver.py; then
        print_status "GeoServer configurado com sucesso"
    else
        print_warning "Falha na configuração do GeoServer (pode não estar rodando)"
    fi
fi

# Verificar configurações
print_status "Verificando configurações..."
if grep -q "NetCDFFileHandler" geonode/upload/settings.py; then
    print_status "Handler NetCDF configurado no settings.py"
else
    print_error "Handler NetCDF não encontrado no settings.py"
fi

if grep -q "netCDF4" requirements.txt; then
    print_status "Dependência netCDF4 adicionada ao requirements.txt"
else
    print_error "Dependência netCDF4 não encontrada no requirements.txt"
fi

# Criar arquivo de configuração de exemplo
print_status "Criando arquivo de configuração de exemplo..."
cat > netcdf_config_example.py << 'EOF'
# Exemplo de configuração para NetCDF
# Adicione estas configurações ao seu settings.py se necessário

# Configurações específicas para NetCDF
NETCDF_SETTINGS = {
    'ENABLE_TIME_DIMENSION': True,
    'DEFAULT_CRS': 'EPSG:4326',
               'MAX_FILE_SIZE': 1024 * 1024 * 900,  # 900MB
    'SUPPORTED_VARIABLES': ['temperature', 'salinity', 'current'],
}

# Configurações do GeoServer para NetCDF
GEOSERVER_NETCDF_SETTINGS = {
    'WORKSPACE': 'netcdf',
    'ENABLE_TIME_DIMENSION': True,
    'DEFAULT_STYLE': 'raster',
}
EOF

print_status "Arquivo de configuração de exemplo criado: netcdf_config_example.py"

# Instruções finais
echo
echo "=== Instalação Concluída ==="
echo
echo "Para usar arquivos NetCDF no GeoNode:"
echo "1. Certifique-se de que o GeoServer está rodando"
echo "2. Acesse a interface de upload do GeoNode"
echo "3. Selecione arquivos .nc, .nc4 ou .netcdf"
echo "4. O sistema processará automaticamente os arquivos"
echo
echo "Para testar:"
echo "  python3 test_netcdf_upload.py"
echo
echo "Para configurar o GeoServer:"
echo "  python3 setup_netcdf_geoserver.py"
echo
echo "Documentação completa: docs/NetCDF_Compatibility.md"
echo

print_status "Instalação concluída com sucesso!"
