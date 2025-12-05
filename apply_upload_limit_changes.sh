#!/bin/bash

# Script para aplicar as mudanças de limite de upload
# Este script deve ser executado após as alterações nos arquivos de configuração

echo "🚀 Aplicando mudanças para aumentar o limite de upload para 900MB..."

# Verificar se estamos no diretório correto
if [ ! -f "geonode/settings.py" ]; then
    echo "❌ Erro: Execute este script no diretório raiz do projeto GeoNode"
    exit 1
fi

echo "📋 Resumo das mudanças aplicadas:"
echo "   • geonode/settings.py: DEFAULT_MAX_UPLOAD_SIZE = 900MB"
echo "   • install_netcdf_support.sh: MAX_FILE_SIZE = 900MB"
echo "   • docker-compose-netcdf.yml: Configuração do nginx adicionada"
echo "   • .env_dev: Variáveis de ambiente para upload"
echo "   • nginx-upload-limit.conf: Configuração do nginx criada"

echo ""
echo "🔧 Próximos passos:"
echo "   1. Reconstruir os containers Docker:"
echo "      docker-compose -f docker-compose-netcdf.yml down"
echo "      docker-compose -f docker-compose-netcdf.yml build --no-cache"
echo "      docker-compose -f docker-compose-netcdf.yml up -d"
echo ""
echo "   2. Executar o script de atualização do banco de dados:"
echo "      python update_upload_limits.py"
echo ""
echo "   3. Verificar se os serviços estão funcionando:"
echo "      docker-compose -f docker-compose-netcdf.yml ps"
echo ""
echo "   4. Testar o upload de um arquivo NetCDF maior que 100MB (até 900MB)"
echo ""
echo "✅ Configurações aplicadas com sucesso!"
echo "   O limite de upload agora é de 900MB para arquivos NetCDF"
