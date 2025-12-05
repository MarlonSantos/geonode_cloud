# ram-otn-deploy
Playbooks Ansible para instalação dos sistemas da OTN no servidor RAM-BR

#  Guia de instalação local do Geonode via Ansible
Esta documentação detalha como utilizar a automatização Ansible desenvolvida para instalação do GeoNode no projeto RAM-BR.

## Primeiro passo: Subir o GeoNode em um servidor local
### Preparação do Ambiente
Instalação do Ansible na Máquina de Controle

```
# Atualize o sistema
sudo apt update && sudo apt upgrade -y

# Instale os pacotes de softwares essenciais
sudo apt install software-properties-common

# Adicione o repositório do Ansible
sudo add-apt-repository --yes --update ppa:ansible/ansible

# Instale o Ansible
sudo apt install ansible

# Verifique a versão de instalação
ansible --version
```

### Obtenção dos Arquivos

```
# Clonar o repositório
git clone https://github.com/ram-brasil/ram-otn-deploy.git

# Entrar no diretório
cd ram-otn-deploy
```

### Estrutura dos Arquivos
A automatização está organizada da seguinte forma:

```
📁 projeto-ansible/
├── ⚙️ ansible.cfg
├── 🖥️ hosts.ini
├── 📋 playbook.yml
└── 📁 roles/
    ├── 🐳 1_docker_setup/
    ├── 🌍 2_geonode_project/
    └── 🚀 3_geonode_deploy/
```


### Configuração dos Arquivos principais
Configure o arquivo de configuração do ansible (⚙️ **ansible.cfg**):

```
[defaults]
host_key_checking = False
inventory = hosts.ini
remote_user = ram
timeout = 30
gathering = smart
fact_caching = memory
stdout_callback = yaml
roles_path = ./roles

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s
pipelining = True
```

Configure o inventário (🖥️**hosts.ini**) com os dados do servidor:

```
[ram-br]
192.168.186.131

[ram-br:vars]
ansible_user=ram
ansible_ssh_private_key_file=~/.ssh/id_rsa
ansible_become=yes
ansible_become_method=sudo
ansible_become_pass=123
```

Configure as variáveis do projeto (📋 **playbook.yml**):


- `--geonode_project_name` : Nome do projeto
- `--env_type`: Está definido para produção. O Letsencrypt usa um e-mail para emitir o certificado SSL
- `--vm_ip`: A URL que servirá o GeoNode (IP do servidor por padrão)
- `--geonode_admin_password`: Senha do admin do Geonode
- `--geoserver_admin_password`: Senha do admin do GeoServer
- `--postgres_password`: Senha do usuário postgres (PostgresSQL)
- `--db_password`: Senha do banco de dados geonode do Geonode (PostgresSQL)
- `--geodb_password`: Senha do banco de dados geonode_data do Geonode (PostgresSQL)
- `--admin_email`: O e-mail do administrador. Observe que são necessários um e-mail real e uma configuração SMTP válida.
- `--geonode_branch`: Versão do Geonode (Estável)



### Preparação do Servidor de Destino
Configuração de Acesso SSH

```
# Gere a chave SSH (se não existir)
ssh-keygen -t rsa -b 4096

# Copie chave para o servidor
ssh-copy-id ram@192.168.186.131

# Teste a conectividade
ssh ram@192.168.186.131
```

Teste de Conectividade Ansible

```
# Teste via ping
ansible ram-br -m ping

# Verifique a conectividade
ansible ram-br -m setup
```

### Execução da Automatização do ansible
```
#Execute o playbook criado no terminal
ansible-playbook -i hosts.ini playbook.yml -v
```


## Segundo passo: Implementar o GeoNode em um servidor de produção (Necessário configuração manual via ssh)

### Caso você queira o serviço em, digamos, https://my_geonode.geonode.org/, você precisará alterar .env no servidor da seguinte forma:

```
DOCKER_ENV=production
SITEURL=https://my_geonode.geonode.org/
NGINX_BASE_URL=https://my_geonode.geonode.org/
ALLOWED_HOSTS=['django',]
GEOSERVER_WEB_UI_LOCATION=https://my_geonode.geonode.org/geoserver/
GEOSERVER_PUBLIC_LOCATION=https://my_geonode.geonode.org/geoserver/
HTTP_HOST=
HTTPS_HOST=my_geonode.geonode.org
HTTP_PORT=80
HTTPS_PORT=443
LETSENCRYPT_MODE=production # Isso usará o Letsencrypt e o servidor ACME para gerar certificados SSL válidos
```

⚠️ Quando LETSENCRYPT_MODE é definido como produção, um e-mail válido e um servidor SMTP de e-mail são necessários para que o sistema gere um certificado válido.

### Reinicie os containers
#### Sempre que você alterar algo no arquivo .env, você precisará reconstruir o containers

Lembrando que o comando a seguir descarta qualquer alteração que você possa ter feito manualmente dentro dos containers, exceto para os volumes estáticos.

```
docker-compose up -d
```
