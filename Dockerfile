FROM geonode/geonode-base:latest-ubuntu-22.04
LABEL GeoNode development team

COPY . /usr/src/geonode/
WORKDIR /usr/src/geonode

COPY wait-for-databases.sh /usr/bin/wait-for-databases
RUN chmod +x /usr/bin/wait-for-databases
RUN chmod +x /usr/src/geonode/tasks.py \
    && chmod +x /usr/src/geonode/entrypoint.sh

COPY celery.sh /usr/bin/celery-commands
RUN chmod +x /usr/bin/celery-commands

COPY celery-cmd /usr/bin/celery-cmd
RUN chmod +x /usr/bin/celery-cmd

# # Install "geonode-contribs" apps
# RUN cd /usr/src; git clone https://github.com/GeoNode/geonode-contribs.git -b master
# # Install logstash and centralized dashboard dependencies
# RUN cd /usr/src/geonode-contribs/geonode-logstash; pip install --upgrade  -e . \
#     cd /usr/src/geonode-contribs/ldap; pip install --upgrade  -e .

RUN yes w | pip install --src /usr/src -r requirements.txt &&\
    yes w | pip install -e .

RUN apt-get autoremove --purge &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Customizações -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
COPY /geonode_custom/mapstore/gn-translations/data.pt-BR.json /usr/local/lib/python3.10/dist-packages/geonode_mapstore_client/static/mapstore/gn-translations/data.pt-BR.json
COPY /geonode_custom/mapstore/ms-translations/data.pt-BR.json /usr/local/lib/python3.10/dist-packages/geonode_mapstore_client/static/mapstore/ms-translations/data.pt-BR.json
COPY /geonode_custom/locale/pt_BR/LC_MESSAGES/django.po /usr/src/geonode/geonode/locale/pt_BR/LC_MESSAGES/django.po
COPY /geonode_custom/static/icon/ /usr/src/geonode/geonode/static/icon/
COPY /geonode_custom/static/img/ /usr/src/geonode/geonode/static/img/
COPY /geonode_custom/mapstore/templates/ /usr/local/lib/python3.10/dist-packages/geonode_mapstore_client/templates/
COPY /geonode_custom/mapstore/css/geonode_override.css /usr/local/lib/python3.10/dist-packages/geonode_mapstore_client/static/mapstore/dist/themes/geonode_override.css
# NetCDF Fix - Removidos scripts antigos que causavam conflitos
# NetCDF DEFINITIVE FIX: Template com solução definitiva
COPY /geonode_custom/mapstore/templates/geonode-mapstore-client/_geonode_config.html /usr/local/lib/python3.10/dist-packages/geonode_mapstore_client/templates/geonode-mapstore-client/_geonode_config.html
# NetCDF BACKEND FIX: Handler definitivo para NetCDF
COPY /geonode/upload/handlers/netcdf/definitive_handler.py /usr/local/lib/python3.10/dist-packages/geonode/upload/handlers/netcdf/definitive_handler.py
# NetCDF SETTINGS FIX: Configuração de handlers
COPY /geonode/upload/settings.py /usr/local/lib/python3.10/dist-packages/geonode/upload/settings.py
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

EXPOSE 8000

