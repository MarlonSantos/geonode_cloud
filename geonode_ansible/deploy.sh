#!/bin/bash
set -e

echo "=== Deploy ReNOMO GeoNode ==="

# === Função para instalar Python automaticamente ===
install_python() {
    echo "Python3 não encontrado. Tentando instalar..."

    if [ -x "$(command -v apt)" ]; then
        sudo apt update && sudo apt install -y python3 python3-pip
    elif [ -x "$(command -v dnf)" ]; then
        sudo dnf install -y python3 python3-pip
    elif [ -x "$(command -v yum)" ]; then
        sudo yum install -y python3 python3-pip
    elif [ -x "$(command -v apk)" ]; then
        sudo apk add --no-cache python3 py3-pip
    else
        echo "Gerenciador de pacotes não suportado. Instale o Python manualmente."
        exit 1
    fi

    # Verifica novamente se a instalação funcionou
    if ! command -v python3 >/dev/null 2>&1; then
        echo "Falha ao instalar o Python3. Instale manualmente e tente novamente."
        exit 1
    fi

    echo "Python3 instalado com sucesso!"
}

# === Função para instalar Ansible automaticamente ===
install_ansible() {
    echo "Ansible não encontrado. Tentando instalar..."

    if [ -x "$(command -v apt)" ]; then
        sudo apt update && sudo apt install -y ansible
    elif [ -x "$(command -v dnf)" ]; then
        sudo dnf install -y ansible
    elif [ -x "$(command -v yum)" ]; then
        sudo yum install -y ansible
    elif [ -x "$(command -v apk)" ]; then
        sudo apk add --no-cache ansible
    else
        echo "Gerenciador de pacotes não suportado. Instale o Ansible manualmente."
        exit 1
    fi

    # Verifica novamente se a instalação funcionou
    if ! command -v ansible >/dev/null 2>&1; then
        echo "Falha ao instalar o Ansible. Instale manualmente e tente novamente."
        exit 1
    fi

    echo "Ansible instalado com sucesso!"
}


# === Função para verificar pré-requisitos ===
check_prerequisites() {
    echo "Verificando pré-requisitos..."
    
    # Verificar se usuário tem sudo
    if ! sudo -n true 2>/dev/null; then
        echo "AVISO: Usuário pode não ter privilégios sudo completos"
        echo "Certifique-se de que o usuário está no grupo sudo"
    fi
    
    # Verificar se config.yml existe
    if [ ! -f "config.yml" ]; then
        echo "ERRO: Arquivo config.yml não encontrado!"
        echo "Copie config.yml.example para config.yml e edite"
        exit 1
    fi
    
    # Verificar conectividade básica
    local hostname=$(grep -A1 "hostname:" config.yml | tail -1 | tr -d ' "')
    if [ -n "$hostname" ] && [ "$hostname" != "localhost" ]; then
        echo "Verificando conectividade com $hostname..."
        if ! ping -c 1 "$hostname" >/dev/null 2>&1; then
            echo "AVISO: Não é possível fazer ping para $hostname"
            echo "Verifique se o servidor está acessível"
        fi
    fi
}

# === Função para validar configuração ===
validate_config() {
    echo "Validando configuração..."
    
    # Verificar se Python está disponível para validação
    if command -v python3 >/dev/null 2>&1; then
        python3 -c "
import yaml
import sys

try:
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
    
    required_sections = ['server', 'project', 'network', 'passwords']
    missing_sections = []
    
    for section in required_sections:
        if section not in config:
            missing_sections.append(section)
    
    if missing_sections:
        print(f'ERRO: Seções ausentes em config.yml: {missing_sections}')
        sys.exit(1)
    
    # Verificar campos obrigatórios
    required_fields = {
        'server': ['hostname', 'user'],
        'project': ['name', 'branch', 'env_type'],
        'network': ['hostname', 'http_port', 'https_port'],
        'passwords': ['geonode_admin', 'geoserver_admin', 'postgres']
    }
    
    for section, fields in required_fields.items():
        if section in config:
            for field in fields:
                if field not in config[section]:
                    print(f'ERRO: Campo obrigatório ausente: {section}.{field}')
                    sys.exit(1)
    
    print('✓ Configuração válida!')
    
except Exception as e:
    print(f'ERRO na validação: {e}')
    sys.exit(1)
"
    else
        echo "AVISO: Python não disponível para validação completa"
    fi
}

# === Função para verificar se Python3 está instalado ===
if ! command -v python3 >/dev/null 2>&1; then
    install_python
else
    echo "Python3 encontrado: $(python3 --version)"
fi

# === Função para verificar se Ansible está instalado ===
if ! command -v ansible >/dev/null 2>&1; then
    install_ansible
else
    echo "Ansible encontrado: $(ansible --version | head -1)"
fi

# === Verificar pré-requisitos ===
check_prerequisites

# === Validar configuração ===
validate_config

# === Gera hosts.ini dinamicamente ===
echo "Gerando hosts.ini..."
python3 generate_hosts.py config.yml

# === Função principal de deploy ===
deploy_geonode() {
    echo "Executando deploy..."
    ansible-playbook -i hosts.ini playbook.yml
    echo "Deploy concluído!"
}

# === Função para verificar sintaxe ===
check_syntax() {
    echo "Verificando sintaxe do playbook..."
    ansible-playbook --syntax-check playbook.yml
    echo "✓ Sintaxe OK!"
}

# === Executa baseado nos argumentos ===
if [[ "$1" == "--dry-run" ]]; then
    echo "Modo dry-run - verificando sintaxe..."
    check_syntax
elif [[ "$1" == "--run" ]]; then
    deploy_geonode
elif [[ "$1" == "--auto" ]]; then
    echo "Modo automático - executando deploy completo..."
    deploy_geonode
elif [[ "$1" == "--validate" ]]; then
    echo "Modo validação - verificando configuração..."
    check_syntax
    echo "✓ Validação completa OK!"
else
    echo "Uso: $0 [--dry-run|--run|--auto|--validate]"
    echo ""
    echo "Opções:"
    echo "  --dry-run: Verifica sintaxe sem executar"
    echo "  --run: Executa o deploy"
    echo "  --auto: Executa deploy completo (recomendado para VMs novas)"
    echo "  --validate: Valida configuração e sintaxe"
    echo ""
    echo "Para VMs recém-criadas, use: ./deploy.sh --auto"
    echo ""
    echo "Exemplo de uso:"
    echo "  ./deploy.sh --validate  # Primeiro, valide a configuração"
    echo "  ./deploy.sh --auto      # Depois, execute o deploy"
    exit 1
fi