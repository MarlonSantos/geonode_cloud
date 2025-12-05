# Guia de Deployment

## Pré-requisitos
- Ubuntu 22.04+
- Python 3.12+
- Ansible 2.15+

## Configuração Inicial
1. Clone o repositório
2. Configure o ambiente: `./geonode_ansible/manage_env.sh dev`
3. Edite `geonode_ansible/config.yml`
4. Execute: `./geonode_ansible/deploy.sh --auto`

## Ambientes Disponíveis
- **dev**: Desenvolvimento local
- **staging**: Testes e homologação
- **prod**: Produção

## Troubleshooting
- [Problemas comuns](#problemas-comuns)
- [Logs e debugging](#logs)