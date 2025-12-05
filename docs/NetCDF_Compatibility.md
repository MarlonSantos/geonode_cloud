# Compatibilidade NetCDF no GeoNode

Este documento descreve como configurar e usar arquivos NetCDF no GeoNode, incluindo a integração com o GeoServer.

## Visão Geral

O GeoNode agora suporta nativamente arquivos NetCDF (Network Common Data Form), permitindo:

- Upload direto de arquivos `.nc`, `.nc4`, `.netcdf`
- Extração automática de metadados
- Suporte a dimensões temporais
- Integração com GeoServer para visualização
- Processamento de dados científicos

## Pré-requisitos

### 1. Dependências Python

Adicione as seguintes dependências ao seu ambiente:

```bash
pip install netCDF4>=1.6.0
```

### 2. Plugins GeoServer

Certifique-se de que os seguintes plugins estão instalados no GeoServer:

- `geoserver-2.24.4-netcdf-plugin.zip`

## Configuração

### 1. Configurações do GeoNode

As configurações para NetCDF já estão incluídas no `settings.py`:

```python
# Adicionar suporte para formatos NetCDF e GRIB
ADDITIONAL_DATASET_FILE_TYPES = [
    {
        "id": "netcdf",
        "label": "NetCDF",
        "formats": [
            {
                "label": "NetCDF File",
                "required_ext": ["nc", "netcdf"],
                "optional_ext": [],
            }
        ],
        "actions": ["upload", "replace"],
        "type": "raster",
    },
    # ... outras configurações
]

# Atualizar a configuração UPLOADER
UPLOADER = {
    "BACKEND": "geonode.importer",
    "OPTIONS": {
        "TIME_ENABLED": True,
        "MOSAIC_ENABLED": False,
    },
    "SUPPORTED_EXT": [
        ".shp", ".csv", ".kml", ".kmz", ".json", ".geojson", 
        ".tif", ".tiff", ".geotiff", ".gml", ".xml",
        ".nc", ".netcdf", ".grib", ".grb", ".grib2", ".grb2"
    ],
}
```

### 2. Handler NetCDF

O handler NetCDF (`geonode/upload/handlers/netcdf/`) inclui:

- **Validação**: Verifica estrutura do arquivo, dimensões espaciais e variáveis
- **Extração de metadados**: Título, descrição, variáveis, dimensões
- **Suporte temporal**: Identifica e processa dimensões de tempo
- **Integração GeoServer**: Publica automaticamente no GeoServer

### 3. Configuração do GeoServer

Execute o script de configuração:

```bash
python setup_netcdf_geoserver.py
```

Este script:
- Verifica se o GeoServer está rodando
- Confirma a presença dos plugins NetCDF
- Cria workspace específico para NetCDF
- Configura coverage stores
- Faz upload de arquivos de exemplo

## Uso

### 1. Upload via Interface Web

1. Acesse a interface de upload do GeoNode
2. Selecione arquivos `.nc`, `.nc4` ou `.netcdf`
3. O sistema automaticamente:
   - Valida o arquivo
   - Extrai metadados
   - Publica no GeoServer
   - Cria recursos no GeoNode

### 2. Upload via API

```python
import requests

# Configurações
upload_url = "http://localhost:8000/api/v2/uploads/upload/"
files = {'base_file': open('dados.nc', 'rb')}
data = {'time_enabled': 'true'}

# Upload
response = requests.post(
    upload_url,
    auth=('username', 'password'),
    files=files,
    data=data
)
```

### 3. Upload via Linha de Comando

```bash
python manage.py importlayers --user=admin --file=dados.nc
```

## Estrutura de Arquivos NetCDF Suportada

### Dimensões Obrigatórias

O arquivo NetCDF deve ter pelo menos 2 dimensões espaciais:

- **Latitude**: `lat`, `latitude`, `y`
- **Longitude**: `lon`, `longitude`, `x`

### Dimensões Opcionais

- **Tempo**: `time`, `date`, `temporal`
- **Profundidade**: `depth`, `level`, `z`
- **Outras**: Qualquer dimensão adicional

### Variáveis

- Pelo menos uma variável de dados
- Variáveis de coordenadas (lat, lon, time)
- Atributos globais e de variáveis

## Metadados Extraídos

O handler automaticamente extrai:

### Metadados Globais
- `title`: Título do dataset
- `description`: Descrição
- `history`: Histórico de processamento
- Outros atributos globais

### Informações de Variáveis
- Nome e tipo de dados
- Dimensões
- Unidades
- Descrição longa

### Dimensões Temporais
- Nome da dimensão de tempo
- Número de passos temporais
- Unidades de tempo
- Calendário

## Visualização

### 1. GeoServer

Os dados NetCDF são publicados como:

- **Coverage Stores**: Para dados raster
- **WMS/WCS**: Serviços OGC
- **Time Dimension**: Suporte a animações temporais

### 2. GeoNode

- Metadados completos
- Visualização em mapas
- Download de dados
- Compartilhamento

## Exemplos

### Arquivo NetCDF Simples

```python
import netCDF4
import numpy as np

# Criar arquivo de exemplo
with netCDF4.Dataset('exemplo.nc', 'w') as nc:
    # Dimensões
    nc.createDimension('time', 10)
    nc.createDimension('lat', 180)
    nc.createDimension('lon', 360)
    
    # Variáveis
    times = nc.createVariable('time', 'f8', ('time',))
    lats = nc.createVariable('lat', 'f4', ('lat',))
    lons = nc.createVariable('lon', 'f4', ('lon',))
    temp = nc.createVariable('temperature', 'f4', ('time', 'lat', 'lon'))
    
    # Dados
    times[:] = np.arange(10)
    lats[:] = np.linspace(-90, 90, 180)
    lons[:] = np.linspace(-180, 180, 360)
    temp[:] = np.random.rand(10, 180, 360)
    
    # Atributos
    nc.title = 'Dados de Temperatura'
    temp.units = 'celsius'
    times.units = 'days since 2020-01-01'
```

### Teste do Handler

```bash
python test_netcdf_upload.py
```

## Troubleshooting

### Problemas Comuns

1. **Plugin não encontrado**
   - Verifique se os plugins NetCDF estão instalados no GeoServer
   - Reinicie o GeoServer após instalação

2. **Erro de validação**
   - Verifique se o arquivo tem dimensões espaciais
   - Confirme que há pelo menos uma variável de dados

3. **Falha no upload**
   - Verifique permissões de arquivo
   - Confirme que o GeoServer está acessível
   - Verifique logs do GeoNode e GeoServer

### Logs

- **GeoNode**: `logs/geonode.log`
- **GeoServer**: `logs/geoserver.log`
- **Upload**: Interface de upload do GeoNode

## Desenvolvimento

### Estrutura do Handler

```
geonode/upload/handlers/netcdf/
├── __init__.py
├── apps.py
├── exceptions.py
├── handler.py
└── tests.py
```

### Extensões

Para adicionar suporte a novos formatos:

1. Crie novo handler em `handlers/`
2. Adicione à lista `SYSTEM_HANDLERS`
3. Configure extensões em `settings.py`
4. Implemente validação e processamento

### Testes

Execute os testes:

```bash
python -m pytest geonode/upload/handlers/netcdf/tests.py -v
```

## Referências

- [NetCDF Documentation](https://www.unidata.ucar.edu/software/netcdf/)
- [GeoServer NetCDF Plugin](https://docs.geoserver.org/stable/en/user/extensions/netcdf/index.html)
- [GeoNode Upload Documentation](https://docs.geonode.org/en/master/usage/upload/index.html)

## Suporte

Para problemas ou dúvidas:

1. Verifique a documentação
2. Consulte os logs
3. Teste com arquivos de exemplo
4. Abra uma issue no repositório
