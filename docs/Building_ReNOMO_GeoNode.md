## Introdução

GeoNode é uma plataforma de código aberto que facilita a gestão e publicação de dados geoespaciais. Ela integra várias funcionalidades para criar, compartilhar e colaborar em dados espaciais.

O GeoNode é construído principalmente em Python/Django.

### Principais Funcionalidades do GeoNode:

- **Gerenciamento de Dados**: Permite o upload, armazenamento e gerenciamento de vários formatos de dados geoespaciais, incluindo shapefiles, GeoTIFF e outros.
- **Criação de Mapas**: Fornece ferramentas para criar mapas interativos usando camadas de dados geoespaciais carregadas.
- **Colaboração**: Suporta fluxos de trabalho colaborativos, permitindo que os usuários compartilhem dados e mapas com outros, controlem permissões de acesso e rastreiem mudanças.
- **Gestão de Metadados**: Integra capacidades de criação e edição de metadados, garantindo que os dados sejam bem documentados e facilmente descobertos.
- **Interoperabilidade**: Suporta serviços geoespaciais padrão como Web Map Service (WMS), Web Feature Service (WFS) e Catalogue Service for the Web (CSW), garantindo compatibilidade com outras ferramentas SIG.

---

### Estrutura Geral do GeoNode

A aplicação GeoNode foi configurada utilizando contêineres Docker para facilitar a implantação e manutenção. Abaixo estão os principais componentes e sua função:

## Principais Contêineres

### 1. `django4geonode`
- **Descrição**: Contêiner principal que executa o backend Django do GeoNode, responsável por gerenciar operações do sistema como autenticação, APIs REST e integração com o banco de dados.
- **Funções Importantes**:
  - Instalação e configuração de dependências como `GDAL` e `libgdal-dev`.
  - Configuração de diretórios estáticos e arquivos personalizados.
  - Execução de scripts de inicialização e migração do banco de dados.
- **Diretórios Configurados**:
  - `static`: Diretórios para ativos estáticos (CSS, JS, imagens).
  - `uploaded`: Diretório para uploads de arquivos dos usuários.
  - `logs`: Diretório para armazenamento de logs do sistema.

### 2. `celery4geonode`
- **Descrição**: Gerencia tarefas assíncronas, como processamento de dados e envio de notificações.
- **Configurações**:
  - Scripts customizados para iniciar o Celery.
  - Logs de tarefas em `/var/log/celery.log`.

### 3. `db4geonode`
- **Descrição**: Banco de dados PostgreSQL com suporte à extensão PostGIS.
- **Função**: Armazena informações sobre camadas geoespaciais, usuários, permissões, configurações e logs de transações.

### 4. `rabbitmq4geonode`
- **Descrição**: Sistema de mensageria utilizado pelo Celery para gerenciar tarefas em fila.
- **Função**: Garante a comunicação entre o backend e as tarefas em segundo plano.

### 5. `nginx4geonode`
- **Descrição**: Servidor web responsável por servir os recursos estáticos e encaminhar requisições ao backend Django.
- **Configuração**: Otimizado para manipular grandes volumes de dados geoespaciais.

### 6. `geoserver4geonode`
- **Descrição**: Publica e serve camadas geoespaciais utilizando serviços padrão OGC como WMS, WFS e CSW.
- **Integração com GeoNode**: Serve como backend para visualização e edição de dados geoespaciais.

### 7. `memcached4geonode`
- **Descrição**: Sistema de cache em memória para acelerar consultas frequentes no GeoNode.

### 8. `letsencrypt4geonode`
- **Descrição**: Gerencia certificados SSL para fornecer conexões seguras ao GeoNode.

---

### DevOps - Pricipais Comandos

### 1. `Build`
```bash
docker-compose up --build
```
### 2. `Restart`
```bash
docker-compose restart <NOME_DO_CONTEINER>
```
ou, para todos os serviços: 
```bash
docker-compose restart 
```

### 3. `Unbuild`
```bash
docker-compose down -v
```

### 4. `Listar Containers Ativos`
```bash
docker ps
```
ou, para todos os containers: 
```bash
docker ps -a
```

### 5. `Entrar num Container`
```bash
docker-compose exec <NOME_DO_CONTEINER> bash
```

---

### Customização

Os arquivos customizados substituem os originais durante a build. Tais arquivos estão em no diretório "geonode_custom".


---

### Problemas (Troubleshooting)


#### SSH:
Troque id_ed25519 pelo seu id ssh

```bash
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_ed25519
ssh -T git@github.com
```

#### Reiniciando todos os serviços:
```bash
docker-compose down --volumes
```
```bash
docker-compose up --build
```

#### Log do Geonode 
```bash
docker exec -it django4geonode cat /var/log/geonode.log
```

#### "container django4geonode is unhealthy"

O mais frequente é a porta escolhida permanecer ocupada. 

Verificação rápida:
```bash
docker exec -it django4geonode python manage.py check
```

Verificação completa:

1 - Verificar o DB: 
```bash
docker-compose exec db psql -U postgres
```
Caso entre no Postgre, tudo certo.

2 - Verificar Django: 

2.1 - Entrar no container:
```bash
docker exec -it django4geonode bash
```
2.2 - Verificar instalação:
```bash
python manage.py check
```
Caso necessário, refaça a migração:
```bash
python manage.py migrate
```
2.3 - Teste o servidor:
```bash
python manage.py runserver 0.0.0.0:8000
```
2.4 - Listando os processos no container
```bash
ps aux | grep manage.py
```
2.5 - Identificando quem está ocupando a porta
```bash
apt update && apt install -y lsof
lsof -ti :8000 | xargs kill -9
```
2.6 - Desoocupando a porta
<PID> = Id identificado no item 2.4.
```bash
kill -9 <PID>
```
2.7 - Reiniciando o servidor
```bash
python manage.py runserver 0.0.0.0:8000
```

#### failed to solve: geonode/geonode-base:latest-ubuntu-22.04: failed to resolve source metadata for docker.io/geonode/geonode-base:latest-ubuntu-22.04
1 - Verificar conexão com Docker Hub
```bash
ping hub.docker.com
```
2 - Verificar disponibilidade da imagem
```bash
docker pull geonode/geonode-base:latest-ubuntu-22.04
```
3 - Tentar novamente a build
```bash
docker-compose up --build
```
Caso não haja mais diponibilidade, o "FROM" no dockerfile deve ser atualizado.

#### Error response from daemon: error while removing network: network geonode_default id 

1 - Reiniciar o Docker
Linux
```bash
sudo systemctl restart docker
```
WSL
restartar o Docker Desktop, e depois o WSL
```bash
wsl --shutdown
wsl
```
2 - Verificar se a rede geonode_default ainda está ativa (se aparece na listagem)
```bash
docker network ls
```
3 - Desativar a rede geonode_default 
```bash
docker network rm geonode_default
```