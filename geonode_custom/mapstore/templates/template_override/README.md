# Template Override - GeoNode MapStore

Esta pasta contém cópias dos templates HTML que precisam ser modificados para que o override do `base.css` funcione corretamente.

**Nota:** A pasta foi renomeada de `template override` para `template_override` para evitar problemas com espaços no Docker.

## Estrutura de Arquivos

### 📁 `geonode-mapstore-client/snippets/head.html`
- **Propósito:** Template do cabeçalho do MapStore
- **Modificação:** Inclui `<link href="{% static 'geonode/css/base_override.css' %}?{% client_version %}" rel="stylesheet" />`
- **Localização original:** `geonode_custom/mapstore/templates/geonode-mapstore-client/snippets/head.html`

### 📁 `base.html`
- **Propósito:** Template base do MapStore
- **Modificação:** Inclui `<link href="{% static 'geonode/css/base_override.css' %}?{% client_version %}" rel="stylesheet" />`
- **Localização original:** `geonode_custom/mapstore/templates/base.html`

### 📁 `geonode_base.html`
- **Propósito:** Template base principal do GeoNode
- **Modificação:** Já inclui o `base_override.css` por padrão
- **Localização original:** `geonode/templates/base.html`

### 📁 `geonode_metadata_full.html`
- **Propósito:** Template de metadados completos do GeoNode
- **Modificação:** Já inclui o `base_override.css` por padrão
- **Localização original:** `geonode/catalogue/templates/geonode_metadata_full.html`

## Como Usar

Para aplicar as modificações:

1. **Copie os arquivos** desta pasta para suas respectivas localizações originais
2. **Ou modifique** os arquivos originais para incluir a linha do `base_override.css`
3. **Reinicie o servidor** para que as mudanças tenham efeito

## CSS Override

O arquivo `base_override.css` contém regras para:
- ✅ Menu esquerdo ativo com texto branco
- ✅ Dropdown do menu direito com texto escuro
- ✅ Sobrescrever regras do Bootstrap

## Ordem de Carregamento

1. `geonode/css/base.css` (original)
2. `geonode/css/base_override.css` (override)
3. `mapstore/dist/themes/geonode.css` (MapStore)
4. `mapstore/dist/themes/geonode_override.css` (MapStore override)

Esta ordem garante que as regras do override tenham prioridade sobre as regras originais. 