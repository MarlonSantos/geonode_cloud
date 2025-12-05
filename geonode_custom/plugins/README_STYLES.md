# Estilos SLD para GeoServer

Este diretório contém estilos SLD (Styled Layer Descriptor) que são automaticamente incluídos durante o build do GeoServer.

## Estilos Disponíveis

### sst_colormap.sld
- **Nome**: sst_colormap
- **Título**: Sea Surface Temperature Delta
- **Tipo**: Raster colormap
- **Descrição**: Estilo para visualização de dados de temperatura da superfície do mar com gradiente de cores do azul (frio) ao vermelho (quente)

#### Especificações do Colormap:
- **0.0**: Azul (#0000ff) - Temperatura mais baixa
- **1.0**: Ciano (#00ffff) - Temperatura baixa
- **2.0**: Verde (#00ff00) - Temperatura média
- **3.0**: Amarelo (#ffff00) - Temperatura alta
- **4.0**: Vermelho (#ff0000) - Temperatura mais alta

## Como Usar

### 1. Aplicar o Estilo a uma Camada Raster

Via Interface Web do GeoServer:
1. Acesse o GeoServer (http://localhost:8080/geoserver)
2. Vá para "Layers" no menu lateral
3. Selecione a camada raster desejada
4. Clique em "Edit"
5. Na seção "Styles", selecione "sst_colormap" da lista
6. Clique em "Save"

### 2. Aplicar via REST API

```bash
# Aplicar o estilo a uma camada específica
curl -u admin:geoserver \
     -X PUT \
     -H "Content-type: application/json" \
     -d '{"layer":{"defaultStyle":{"name":"sst_colormap"}}}' \
     "http://localhost:8080/geoserver/rest/layers/SUA_CAMADA"
```

### 3. Usar em WMS/WMTS

```xml
<!-- Exemplo de requisição WMS com o estilo -->
<GetMap>
  <Layer>SUA_WORKSPACE:SUA_CAMADA</Layer>
  <Style>sst_colormap</Style>
  <!-- outros parâmetros... -->
</GetMap>
```

### 4. Estilo Padrão Automático

O estilo `sst_colormap` é automaticamente aplicado como padrão para:
- **Todas as camadas raster existentes** na inicialização
- **Novas camadas raster** criadas após a inicialização (monitoramento contínuo)

Isso significa que você não precisa aplicar manualmente o estilo - ele será usado automaticamente!

## Instalação Automática

Os estilos são automaticamente:
1. Copiados para `/tmp/styles/` durante o build
2. Transferidos para `/geoserver_data/data/styles/` na inicialização
3. Registrados no GeoServer via REST API
4. **Aplicados como estilo padrão para todas as camadas raster existentes**
5. **Monitoramento contínuo para aplicar automaticamente a novas camadas raster**

## Verificação

Para verificar se o estilo foi registrado corretamente:

```bash
# Listar todos os estilos
curl -u admin:geoserver \
     "http://localhost:8080/geoserver/rest/styles"

# Verificar o estilo específico
curl -u admin:geoserver \
     "http://localhost:8080/geoserver/rest/styles/sst_colormap"
```

## Scripts Disponíveis

### Scripts Automáticos (executados na inicialização):
- **`register_style.sh`**: Registra o estilo no GeoServer
- **`apply_default_style.sh`**: Aplica o estilo como padrão para camadas raster existentes
- **`monitor_new_layers.sh`**: Monitora e aplica o estilo automaticamente a novas camadas raster

### Scripts Manuais:
- **`test_style.sh`**: Testa se o estilo foi registrado corretamente
- **`apply_default_style.sh`**: Aplica o estilo como padrão manualmente (pode ser executado a qualquer momento)

### Executar Scripts Manualmente:
```bash
# Testar se o estilo está funcionando
docker exec -it [container_name] /usr/local/bin/test_style.sh

# Aplicar estilo padrão manualmente
docker exec -it [container_name] /usr/local/bin/apply_default_style.sh

# Iniciar monitoramento manualmente
docker exec -it [container_name] /usr/local/bin/monitor_new_layers.sh
```

## Personalização

Para adicionar novos estilos:

1. Crie o arquivo `.sld` no diretório `geonode_custom/plugins/`
2. Adicione a linha de cópia no `Dockerfile`:
   ```dockerfile
   COPY seu_estilo.sld /tmp/styles/seu_estilo.sld
   ```
3. Modifique o script `register_style.sh` para incluir o novo estilo
4. Rebuild a imagem Docker

## Troubleshooting

### Estilo não aparece na lista
- Verifique se o arquivo SLD foi copiado corretamente
- Confirme se o script de registro foi executado
- Verifique os logs do container

### Erro de sintaxe no SLD
- Valide o XML do arquivo SLD
- Use ferramentas online de validação SLD
- Verifique se todos os namespaces estão corretos

### Estilo não aplica corretamente
- Confirme se a camada é do tipo raster
- Verifique se os valores dos dados estão dentro do range do colormap
- Ajuste os valores `quantity` no SLD conforme necessário
