# geonode_ansible/generate_hosts.py
#!/usr/bin/env python3
import yaml
import sys
import os

def generate_hosts_ini(config_file):
    """Gera o arquivo hosts.ini baseado no config.yml"""
    
    # Lê o arquivo de configuração
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    # Gera o conteúdo do hosts.ini
    hosts_content = f"""[renomo-data1]
{config['server']['hostname']}

[renomo-data1:vars]
ansible_user={config['server']['user']}
ansible_ssh_private_key_file={config['server']['ssh_key']}
ansible_become=yes
ansible_become_method=sudo
ansible_become_pass={config['server']['sudo_password']}
"""
    
    # Escreve o arquivo hosts.ini
    with open('hosts.ini', 'w') as f:
        f.write(hosts_content)
    
    print(f"✓ Arquivo hosts.ini gerado com hostname: {config['server']['hostname']}")

def generate_ansible_cfg(config_file):
    """Gera o arquivo ansible.cfg baseado no config.yml"""
    
    # Lê o arquivo de configuração
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    # Gera o conteúdo do ansible.cfg
    ansible_config = f"""[defaults]
host_key_checking = {str(config['ansible']['host_key_checking']).lower()}
inventory = hosts.ini
remote_user = {config['ansible']['remote_user']}
timeout = {config['ansible']['timeout']}
gathering = {config['ansible']['gathering']}
fact_caching = {config['ansible']['fact_caching']}
stdout_callback = {config['ansible']['stdout_callback']}
roles_path = {config['ansible']['roles_path']}
forks = {config['ansible']['forks']}
retry_files_enabled = {str(config['ansible']['retry_files_enabled']).lower()}
display_skipped_hosts = {str(config['ansible']['display_skipped_hosts']).lower()}
display_ok_hosts = {str(config['ansible']['display_ok_hosts']).lower()}
display_failed_hosts = {str(config['ansible']['display_failed_hosts']).lower()}
verbosity = {config['ansible']['verbosity']}

[ssh_connection]
ssh_args = {config['ansible']['ssh_args']}
pipelining = {str(config['ansible']['pipelining']).lower()}
"""
    
    # Escreve o arquivo ansible.cfg
    with open('ansible.cfg', 'w') as f:
        f.write(ansible_config)
    
    print(f"✓ Arquivo ansible.cfg gerado")

def main():
    """Função principal que gera ambos os arquivos"""
    config_file = sys.argv[1] if len(sys.argv) > 1 else 'config.yml'
    
    if not os.path.exists(config_file):
        print(f"ERRO: Arquivo {config_file} não encontrado!")
        print("Copie config.yml.example para config.yml e edite")
        sys.exit(1)
    
    try:
        # Gera hosts.ini
        generate_hosts_ini(config_file)
        
        # Gera ansible.cfg
        generate_ansible_cfg(config_file)
        
        print("✓ Configuração Ansible gerada com sucesso!")
        
    except KeyError as e:
        print(f"ERRO: Configuração ausente no {config_file}: {e}")
        print("Verifique se todas as seções estão presentes")
        sys.exit(1)
    except Exception as e:
        print(f"ERRO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()