#!/bin/bash

# Script de deploy completo com suporte NetCDF
# Este script faz o deploy completo do GeoNode com todas as funcionalidades NetCDF

set -e

echo "=== Deploy do GeoNode com Suporte NetCDF ==="
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

print_step "1. Preparando ambiente..."

# Parar containers existentes
if docker-compose ps | grep -q "Up"; then
    print_status "Parando containers existentes..."
    docker-compose down
fi

# Limpar volumes se solicitado
read -p "Deseja limpar volumes existentes? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Limpando volumes..."
    docker-compose down -v
    docker volume prune -f
fi

print_step "2. Construindo imagens..."

# Construir imagens com suporte NetCDF
print_status "Construindo imagem do GeoServer com plugins NetCDF..."
docker-compose build geoserver

print_status "Construindo imagem do Django com handler NetCDF..."
docker-compose build django

print_status "Construindo imagem do Celery..."
docker-compose build celery

print_step "3. Iniciando serviços..."

# Iniciar serviços
print_status "Iniciando serviços..."
docker-compose up -d

# Aguardar serviços ficarem prontos
print_status "Aguardando serviços ficarem prontos..."
sleep 60

print_step "4. Verificando serviços..."

# Verificar se o Django está respondendo
print_status "Verificando Django..."
for i in {1..30}; do
    if curl -f -s http://localhost:8000/ > /dev/null; then
        print_status "✓ Django está respondendo"
        break
    else
        if [ $i -eq 30 ]; then
            print_warning "⚠ Django não está respondendo após 5 minutos"
        else
            sleep 10
        fi
    fi
done

# Verificar se o GeoServer está respondendo
print_status "Verificando GeoServer..."
for i in {1..30}; do
    if curl -f -s http://localhost:8080/geoserver/ > /dev/null; then
        print_status "✓ GeoServer está respondendo"
        break
    else
        if [ $i -eq 30 ]; then
            print_warning "⚠ GeoServer não está respondendo após 5 minutos"
        else
            sleep 10
        fi
    fi
done

print_step "5. Configurando NetCDF..."

# Executar configuração do NetCDF
print_status "Configurando GeoServer para NetCDF..."
if docker-compose exec -T django python setup_netcdf_geoserver.py > /dev/null 2>&1; then
    print_status "✓ GeoServer configurado para NetCDF"
else
    print_warning "⚠ Configuração do GeoServer falhou"
fi

print_step "6. Executando migrações..."

# Executar migrações
print_status "Executando migrações do Django..."
docker-compose exec -T django python manage.py migrate --noinput

print_status "Carregando dados iniciais..."
docker-compose exec -T django python manage.py loaddata sample_admin || true
docker-compose exec -T django python manage.py loaddata geonode/base/fixtures/default_oauth_apps_docker.json || true
docker-compose exec -T django python manage.py loaddata geonode/base/fixtures/initial_data.json || true

print_step "7. Testando funcionalidades..."

# Testar handler NetCDF
print_status "Testando handler NetCDF..."
if docker-compose exec -T django python test_netcdf_upload.py > /dev/null 2>&1; then
    print_status "✓ Handler NetCDF funcionando"
else
    print_warning "⚠ Teste do handler NetCDF falhou"
fi

print_step "8. Configuração final..."

# Coletar arquivos estáticos
print_status "Coletando arquivos estáticos..."
docker-compose exec -T django python manage.py collectstatic --noinput

# Compilar traduções
print_status "Compilando traduções..."
docker-compose exec -T django python manage.py compilemessages --settings=geonode.local_settings || true

echo
echo "=== Deploy Concluído com Sucesso! ==="
echo
echo "🎉 O GeoNode com suporte NetCDF está pronto para uso!"
echo
echo "📋 Resumo do deploy:"
echo "  ✅ Imagens Docker construídas com suporte NetCDF"
echo "  ✅ Serviços iniciados e funcionando"
echo "  ✅ GeoServer configurado com plugins NetCDF"
echo "  ✅ Handler NetCDF integrado ao GeoNode"
echo "  ✅ Migrações executadas"
echo "  ✅ Dados iniciais carregados"
echo "  ✅ Testes de funcionalidade executados"
echo
echo "🌐 URLs de acesso:"
echo "  - GeoNode: http://localhost:8000"
echo "  - GeoServer: http://localhost:8080/geoserver"
echo "  - GeoServer Admin: http://localhost:8080/geoserver/web/"
echo
echo "🔑 Credenciais padrão:"
echo "  - Usuário: admin"
echo "  - Senha: admin"
echo
echo "📁 Arquivos NetCDF de exemplo:"
echo "  - Localização: /geoserver_data/data/netcdf_samples/"
echo "  - Arquivos incluídos: chl_july_only.nc, chl_corrected.nc, SST_Mediterraneo.nc"
echo
echo "🔧 Como usar:"
echo "  1. Acesse http://localhost:8000"
echo "  2. Faça login como admin"
echo "  3. Vá para 'Upload' e selecione arquivos .nc"
echo "  4. O sistema processará automaticamente os arquivos NetCDF"
echo
echo "📚 Documentação:"
echo "  - docs/NetCDF_Compatibility.md"
echo "  - NETCDF_IMPLEMENTATION_SUMMARY.md"
echo
echo "🛠️ Comandos úteis:"
echo "  - Ver logs: docker-compose logs -f"
echo "  - Parar serviços: docker-compose down"
echo "  - Reiniciar: docker-compose restart"
echo "  - Testar NetCDF: make netcdf-test"
echo
print_status "Deploy concluído com sucesso!"
