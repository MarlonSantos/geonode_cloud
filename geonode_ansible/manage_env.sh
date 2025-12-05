# geonode_ansible/manage_env.sh
#!/bin/bash

ENVIRONMENT=${1:-dev}
CONFIG_FILE="config/${ENVIRONMENT}.yml"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Ambiente $ENVIRONMENT não encontrado!"
    exit 1
fi

# Copiar configuração do ambiente
cp "$CONFIG_FILE" config.yml

# Gerar hosts específicos do ambiente
python3 generate_hosts.py config.yml

echo "Ambiente $ENVIRONMENT configurado!"