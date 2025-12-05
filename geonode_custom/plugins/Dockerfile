FROM geonode/geoserver:2.24.4-latest

USER root

# Instalar dependências necessárias para os plugins
RUN apt-get update && apt-get install -y \
    unzip \
    curl \
    libnetcdf-dev \
    libhdf5-dev \
    libgdal-dev \
    gdal-bin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar os plugins
COPY geoserver-2.24.3-netcdf-plugin.zip /tmp/netcdf-plugin.zip
COPY geoserver-2.24.3-netcdf-out-plugin.zip /tmp/netcdf-out-plugin.zip
COPY geoserver-2.24.3-grib-plugin.zip /tmp/grib-plugin.zip

# Verificar se os arquivos dos plugins existem
RUN ls -la /tmp/*.zip

# Extrair TODOS os JARs dos plugins (incluindo bibliotecas nativas)
RUN echo "=== Extraindo plugins completos ===" && \
    mkdir -p /tmp/extracted && \
    # Extrair NetCDF plugin completo
    unzip -q /tmp/netcdf-plugin.zip -d /tmp/extracted/netcdf && \
    find /tmp/extracted/netcdf -name "*.jar" -exec cp {} /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/ \; && \
    # Extrair NetCDF output plugin completo
    unzip -q /tmp/netcdf-out-plugin.zip -d /tmp/extracted/netcdf-out && \
    find /tmp/extracted/netcdf-out -name "*.jar" -exec cp {} /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/ \; && \
    # Extrair GRIB plugin completo
    unzip -q /tmp/grib-plugin.zip -d /tmp/extracted/grib && \
    find /tmp/extracted/grib -name "*.jar" -exec cp {} /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/ \;

# Verificar se os plugins foram instalados
RUN echo "=== Plugins instalados ===" && \
    find /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/ -name "*netcdf*" -o -name "*grib*" | head -10

# Limpar arquivos temporários
RUN rm -rf /tmp/netcdf-plugin.zip /tmp/netcdf-out-plugin.zip /tmp/grib-plugin.zip /tmp/extracted

# Definir permissões corretas
RUN chown -R root:root /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/ && \
    chmod -R 644 /usr/local/tomcat/webapps/geoserver/WEB-INF/lib/*.jar

# # Criar diretório de dados e copiar arquivo NetCDF de exemplo
# RUN mkdir -p /geoserver_data/data && \
    # echo "=== Baixando arquivo NetCDF de exemplo ===" && \
    # curl -L -o /geoserver_data/data/chl_july_only.nc 'https://www.unidata.ucar.edu/software/netcdf/examples/tos_O1_2001-2002.nc' && \
    # echo "=== Arquivo NetCDF copiado com sucesso ===" && \
    # ls -la /geoserver_data/data/chl_july_only.nc

# Criar diretório de dados do GeoServer e copiar arquivo NetCDF
# O volume geoserver-data-dir monta /geoserver_data/data, então copiamos para lá
# RUN echo "=== Criando diretório para volume geoserver-data-dir ===" && \
#     mkdir -p /usr/local/tomcat/webapps/geoserver/data/netcdf_samples/ && \
#     echo "=== Diretório criado, verificando estrutura ===" && \
#     ls -la /usr/local/tomcat/webapps/geoserver/data/ && \
#     echo "=== Verificando se netcdf_samples foi criado ===" && \
#     ls -la /usr/local/tomcat/webapps/geoserver/data/netcdf_samples/

# COPY chl_july_only.nc /usr/local/tomcat/webapps/geoserver/data/netcdf_samples/chl_july_only.nc
# COPY chl_corrected.nc /usr/local/tomcat/webapps/geoserver/data/netcdf_samples/chl_corrected.nc

# # Definir permissões para o arquivo NetCDF
# RUN chmod 644 /usr/local/tomcat/webapps/geoserver/data/netcdf_samples/chl_july_only.nc && \
#     chown root:root /usr/local/tomcat/webapps/geoserver/data/netcdf_samples/chl_july_only.nc

# RUN chmod 644 /usr/local/tomcat/webapps/geoserver/data/netcdf_samples/chl_corrected.nc && \
#     chown root:root /usr/local/tomcat/webapps/geoserver/data/netcdf_samples/chl_corrected.nc

# #/usr/local/tomcat/webapps/geoserver/data
# # Verificar se o arquivo NetCDF foi copiado corretamente
# RUN echo "=== Verificando arquivo NetCDF ===" && \
#     ls -la /usr/local/tomcat/webapps/geoserver/data/netcdf_samples/chl_july_only.nc && \
#     echo "=== Arquivo NetCDF copiado com sucesso para /usr/local/tomcat/webapps/geoserver/data/netcdf_samples/ ==="

# Criar diretório temporário para os arquivos NetCDF
RUN echo "=== Criando diretório temporário para arquivos NetCDF ===" && \
    mkdir -p /tmp/netcdf_samples/ && \
    echo "=== Diretório temporário criado ==="

# Criar diretório temporário para os estilos SLD
RUN echo "=== Criando diretório temporário para estilos SLD ===" && \
    mkdir -p /tmp/styles/ && \
    echo "=== Diretório de estilos temporário criado ==="

# Copiar arquivos NetCDF para o diretório temporário
COPY chl_july_only.nc /tmp/netcdf_samples/chl_july_only.nc
COPY chl_corrected.nc /tmp/netcdf_samples/chl_corrected.nc
COPY SST_Mediterraneo.nc /tmp/netcdf_samples/SST_Mediterraneo.nc

# Copiar estilos SLD para o diretório temporário
COPY sst_colormap.sld /tmp/styles/sst_colormap.sld

# Definir permissões para os arquivos NetCDF
RUN chmod 644 /tmp/netcdf_samples/chl_july_only.nc && \
    chown root:root /tmp/netcdf_samples/chl_july_only.nc && \
    chmod 644 /tmp/netcdf_samples/chl_corrected.nc && \
    chown root:root /tmp/netcdf_samples/chl_corrected.nc

# Definir permissões para os arquivos SLD
RUN chmod 644 /tmp/styles/sst_colormap.sld && \
    chown root:root /tmp/styles/sst_colormap.sld

# Verificar se os arquivos NetCDF foram copiados corretamente
RUN echo "=== Verificando arquivos NetCDF no diretório temporário ===" && \
    ls -la /tmp/netcdf_samples/ && \
    echo "=== Arquivos NetCDF copiados com sucesso para /tmp/netcdf_samples/ ==="

# Verificar se os arquivos SLD foram copiados corretamente
RUN echo "=== Verificando arquivos SLD no diretório temporário ===" && \
    ls -la /tmp/styles/ && \
    echo "=== Arquivos SLD copiados com sucesso para /tmp/styles/ ==="

# Criar script de inicialização para copiar arquivos para o volume
RUN echo '#!/bin/bash' > /usr/local/bin/copy-netcdf-files.sh && \
    echo 'echo "=== Copiando arquivos NetCDF para o volume ==="' >> /usr/local/bin/copy-netcdf-files.sh && \
    echo 'mkdir -p /geoserver_data/data/netcdf_samples/' >> /usr/local/bin/copy-netcdf-files.sh && \
    echo 'cp -r /tmp/netcdf_samples/* /geoserver_data/data/netcdf_samples/' >> /usr/local/bin/copy-netcdf-files.sh && \
    echo 'echo "=== Arquivos NetCDF copiados para /geoserver_data/data/netcdf_samples/ ==="' >> /usr/local/bin/copy-netcdf-files.sh && \
    echo 'ls -la /geoserver_data/data/netcdf_samples/' >> /usr/local/bin/copy-netcdf-files.sh && \
    echo 'echo "=== Copiando estilos SLD para o volume ==="' >> /usr/local/bin/copy-netcdf-files.sh && \
    echo 'mkdir -p /geoserver_data/data/styles/' >> /usr/local/bin/copy-netcdf-files.sh && \
    echo 'cp -r /tmp/styles/* /geoserver_data/data/styles/' >> /usr/local/bin/copy-netcdf-files.sh && \
    echo 'echo "=== Estilos SLD copiados para /geoserver_data/data/styles/ ==="' >> /usr/local/bin/copy-netcdf-files.sh && \
    echo 'ls -la /geoserver_data/data/styles/' >> /usr/local/bin/copy-netcdf-files.sh && \
    chmod +x /usr/local/bin/copy-netcdf-files.sh

# Copiar e configurar o entrypoint personalizado
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Copiar script manual para cópia de arquivos NetCDF
COPY copy_netcdf_files.sh /usr/local/bin/copy_netcdf_files.sh
RUN chmod +x /usr/local/bin/copy_netcdf_files.sh

# Copiar script para registro de estilos
COPY register_style.sh /usr/local/bin/register_style.sh
RUN chmod +x /usr/local/bin/register_style.sh

# Copiar script de teste de estilos
COPY test_style.sh /usr/local/bin/test_style.sh
RUN chmod +x /usr/local/bin/test_style.sh

# Copiar script para aplicar estilo padrão
COPY apply_default_style.sh /usr/local/bin/apply_default_style.sh
RUN chmod +x /usr/local/bin/apply_default_style.sh

# Copiar script de monitoramento de novas camadas
COPY monitor_new_layers.sh /usr/local/bin/monitor_new_layers.sh
RUN chmod +x /usr/local/bin/monitor_new_layers.sh

# Definir o entrypoint personalizado
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]