# Changelog - Adição do Estilo SST Colormap

## Resumo das Modificações

Este changelog documenta as modificações feitas para adicionar o estilo colormap SST (Sea Surface Temperature) ao GeoServer durante o build.

## Arquivos Criados

### 1. `sst_colormap.sld`
- **Descrição**: Arquivo SLD com o estilo colormap para temperatura da superfície do mar
- **Conteúdo**: Define um gradiente de cores do azul (frio) ao vermelho (quente)
- **Valores**: 0.0 (azul) → 1.0 (ciano) → 2.0 (verde) → 3.0 (amarelo) → 4.0 (vermelho)

### 2. `register_style.sh`
- **Descrição**: Script para registrar estilos SLD no GeoServer via REST API
- **Funcionalidades**:
  - Aguarda GeoServer estar disponível (com timeout de 5 minutos)
  - Verifica se o estilo já existe
  - Cria ou atualiza o estilo via REST API
  - Tratamento de erros e logging
  - **Aplica automaticamente o estilo como padrão para camadas raster existentes**

### 3. `test_style.sh`
- **Descrição**: Script de teste para verificar se o estilo foi registrado corretamente
- **Testes**:
  - Conectividade com GeoServer
  - Existência do estilo
  - Presença do arquivo SLD no volume
  - Validação do conteúdo do SLD
  - Listagem de todos os estilos

### 4. `README_STYLES.md`
- **Descrição**: Documentação completa sobre os estilos SLD
- **Conteúdo**:
  - Descrição dos estilos disponíveis
  - Instruções de uso
  - Exemplos de aplicação
  - Troubleshooting

### 5. `apply_default_style.sh`
- **Descrição**: Script para aplicar o estilo como padrão para camadas raster
- **Funcionalidades**:
  - Lista todas as camadas do GeoServer
  - Identifica camadas raster
  - Aplica o estilo sst_colormap como padrão
  - Suporte a workspaces específicos

### 6. `monitor_new_layers.sh`
- **Descrição**: Script para monitorar novas camadas raster
- **Funcionalidades**:
  - Monitoramento contínuo (verifica a cada 60 segundos)
  - Detecta novas camadas automaticamente
  - Aplica o estilo padrão a novas camadas raster
  - Execução em background

## Arquivos Modificados

### 1. `Dockerfile`
**Adições**:
- Criação do diretório temporário para estilos (`/tmp/styles/`)
- Cópia do arquivo `sst_colormap.sld` para o diretório temporário
- Definição de permissões para o arquivo SLD
- Verificação da cópia dos arquivos SLD
- Modificação do script de cópia para incluir estilos
- Cópia dos scripts `register_style.sh` e `test_style.sh`

**Linhas modificadas**:
- Linha ~75: Criação do diretório de estilos
- Linha ~80: Cópia do arquivo SLD
- Linha ~85: Permissões do arquivo SLD
- Linha ~90: Verificação dos arquivos SLD
- Linha ~95: Modificação do script de cópia
- Linha ~105: Cópia dos scripts
- Linha ~110: Cópia do script de aplicação de estilo padrão
- Linha ~115: Cópia do script de monitoramento

### 2. `entrypoint.sh`
**Adições**:
- Cópia de estilos SLD para o volume na inicialização
- Execução do script de registro de estilos em background

**Linhas modificadas**:
- Linha ~20: Cópia de estilos para o volume
- Linha ~270: Execução do script de registro
- Linha ~275: Execução do script de monitoramento

## Fluxo de Execução

1. **Build da Imagem**:
   - Arquivo SLD é copiado para `/tmp/styles/`
   - Scripts são copiados para `/usr/local/bin/`

2. **Inicialização do Container**:
   - Estilos são copiados para `/geoserver_data/data/styles/`
   - Script de registro é executado em background
   - GeoServer aguarda estar disponível
   - Estilo é registrado via REST API
   - **Estilo é aplicado como padrão para camadas raster existentes**
   - **Script de monitoramento é iniciado para novas camadas**

3. **Monitoramento Contínuo**:
   - Script verifica novas camadas a cada 60 segundos
   - Aplica automaticamente o estilo padrão a novas camadas raster
   - Execução em background

4. **Verificação**:
   - Script de teste pode ser executado para validar a instalação

## Como Usar

### Aplicar o Estilo a uma Camada:
1. Acesse o GeoServer (http://localhost:8080/geoserver)
2. Vá para "Layers" → [sua camada raster] → "Edit"
3. Selecione "sst_colormap" na lista de estilos
4. Salve as alterações

### Verificar a Instalação:
```bash
# Executar o script de teste
docker exec -it [container_name] /usr/local/bin/test_style.sh
```

### Aplicar via REST API:
```bash
curl -u admin:geoserver \
     -X PUT \
     -H "Content-type: application/json" \
     -d '{"layer":{"defaultStyle":{"name":"sst_colormap"}}}' \
     "http://localhost:8080/geoserver/rest/layers/SUA_CAMADA"
```

## Próximos Passos

Para adicionar novos estilos:
1. Crie o arquivo `.sld` no diretório `geonode_custom/plugins/`
2. Adicione a linha `COPY novo_estilo.sld /tmp/styles/novo_estilo.sld` no Dockerfile
3. Modifique o script `register_style.sh` para incluir o novo estilo
4. Rebuild a imagem Docker

## Troubleshooting

- **Estilo não aparece**: Verifique os logs do container e execute o script de teste
- **Erro de sintaxe**: Valide o XML do arquivo SLD
- **Timeout**: Aumente o timeout no script `register_style.sh` se necessário
