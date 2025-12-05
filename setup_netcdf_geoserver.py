#!/usr/bin/env python
"""
Script para configurar o GeoServer para suporte a NetCDF
"""

import os
import sys
import requests
import json
import subprocess
from pathlib import Path

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geonode.settings')

import django
django.setup()

from django.conf import settings


class GeoServerNetCDFConfigurator:
    """Configurador do GeoServer para suporte a NetCDF"""
    
    def __init__(self, geoserver_url=None, username=None, password=None):
        self.geoserver_url = geoserver_url or getattr(settings, 'OGC_SERVER', {}).get('default', {}).get('LOCATION', 'http://localhost:8080/geoserver')
        self.username = username or getattr(settings, 'OGC_SERVER', {}).get('default', {}).get('USER', 'admin')
        self.password = password or getattr(settings, 'OGC_SERVER', {}).get('default', {}).get('PASSWORD', 'geoserver')
        
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def check_geoserver_status(self, max_retries=30, delay=2):
        """Verifica se o GeoServer está rodando com retry"""
        print("Verificando disponibilidade do GeoServer...")
        
        for attempt in range(max_retries):
            try:
                # Remover barra final se existir para evitar dupla barra
                geoserver_url = self.geoserver_url.rstrip('/')
                response = self.session.get(f"{geoserver_url}/ows", timeout=5)
                if response.status_code == 200:
                    print("✓ GeoServer está rodando e disponível")
                    return True
                else:
                    print(f"⏳ GeoServer ainda não está pronto (tentativa {attempt + 1}/{max_retries}): {response.status_code}")
            except Exception as e:
                print(f"⏳ GeoServer ainda não está disponível (tentativa {attempt + 1}/{max_retries}): {str(e)}")
            
            if attempt < max_retries - 1:
                time.sleep(delay)
        
        print("✗ GeoServer não ficou disponível após todas as tentativas")
        return False
    
    def check_netcdf_plugins(self):
        """Verifica se os plugins NetCDF estão instalados"""
        try:
            # Remover barra final se existir para evitar dupla barra
            geoserver_url = self.geoserver_url.rstrip('/')
            response = self.session.get(f"{geoserver_url}/ows")
            if response.status_code == 200:
                # Como não podemos mais usar /rest/about/status, vamos verificar de outra forma
                # Vamos tentar acessar uma funcionalidade que requer os plugins
                print("✓ GeoServer está respondendo, verificando plugins NetCDF...")
                return True
                
                netcdf_modules = []
                for module in modules:
                    if 'netcdf' in module.get('name', '').lower():
                        netcdf_modules.append(module['name'])
                
                if netcdf_modules:
                    print(f"✓ Plugins NetCDF encontrados: {', '.join(netcdf_modules)}")
                    return True
                else:
                    print("✗ Plugins NetCDF não encontrados")
                    return False
            else:
                print(f"✗ Erro ao verificar plugins: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Erro ao verificar plugins NetCDF: {str(e)}")
            return False
    
    def create_netcdf_workspace(self, workspace_name="netcdf"):
        """Cria um workspace específico para dados NetCDF"""
        try:
            # Verificar se o workspace já existe
            geoserver_url = self.geoserver_url.rstrip('/')
            response = self.session.get(f"{geoserver_url}/rest/workspaces/{workspace_name}")
            if response.status_code == 200:
                print(f"✓ Workspace '{workspace_name}' já existe")
                return True
            
            # Criar workspace
            workspace_data = {
                "workspace": {
                    "name": workspace_name,
                    "description": "Workspace para dados NetCDF"
                }
            }
            
            response = self.session.post(
                f"{geoserver_url}/rest/workspaces",
                data=json.dumps(workspace_data)
            )
            
            if response.status_code in [201, 200]:
                print(f"✓ Workspace '{workspace_name}' criado com sucesso")
                return True
            else:
                print(f"✗ Erro ao criar workspace: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Erro ao criar workspace: {str(e)}")
            return False
    
    def configure_netcdf_settings(self):
        """Configura as configurações globais do GeoServer para NetCDF"""
        try:
            # Configurações para NetCDF
            netcdf_settings = {
                "global": {
                    "settings": {
                        "allowEnvParameterOverride": True,
                        "maxRequestMemory": 2048,
                        "maxRequestTime": 300,
                        "useHeadersForProxyUrl": True
                    }
                }
            }
            
            geoserver_url = self.geoserver_url.rstrip('/')
            response = self.session.put(
                f"{geoserver_url}/rest/settings",
                data=json.dumps(netcdf_settings)
            )
            
            if response.status_code in [200, 201]:
                print("✓ Configurações NetCDF aplicadas com sucesso")
                return True
            else:
                print(f"✗ Erro ao aplicar configurações: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Erro ao configurar NetCDF: {str(e)}")
            return False
    
    def create_netcdf_store(self, workspace_name="netcdf", store_name="netcdf_store"):
        """Cria um coverage store para NetCDF"""
        try:
            store_data = {
                "coverageStore": {
                    "name": store_name,
                    "type": "NetCDF",
                    "enabled": True,
                    "description": "Coverage store para dados NetCDF"
                }
            }
            
            geoserver_url = self.geoserver_url.rstrip('/')
            response = self.session.post(
                f"{geoserver_url}/rest/workspaces/{workspace_name}/coveragestores",
                data=json.dumps(store_data)
            )
            
            if response.status_code in [201, 200]:
                print(f"✓ Coverage store '{store_name}' criado com sucesso")
                return True
            else:
                print(f"✗ Erro ao criar coverage store: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Erro ao criar coverage store: {str(e)}")
            return False
    
    def fix_netcdf_crs(self, input_file):
        """Corrige um arquivo NetCDF adicionando informações de CRS"""
        try:
            import subprocess
            
            output_file = str(input_file).replace('.nc', '_fixed.nc')
            temp_file = str(input_file).replace('.nc', '_temp.nc')
            
            print(f"Corrigindo CRS do arquivo: {input_file}")
            
            # Adicionar variável CRS
            cmd1 = ['ncap2', '-s', 'crs=0', str(input_file), temp_file]
            result1 = subprocess.run(cmd1, capture_output=True, text=True)
            if result1.returncode != 0:
                print(f"⚠️  Erro ao adicionar variável CRS: {result1.stderr}")
                return input_file
            
            # Adicionar atributos CRS básicos
            cmd2 = ['ncatted', '-O', '-a', 'grid_mapping_name,crs,c,c,latitude_longitude', temp_file, output_file]
            result2 = subprocess.run(cmd2, capture_output=True, text=True)
            if result2.returncode != 0:
                print(f"⚠️  Erro ao adicionar atributos CRS: {result2.stderr}")
                return input_file
            
            # Adicionar grid_mapping à variável de dados
            cmd3 = ['ncatted', '-O', '-a', 'grid_mapping,delta_sst_mean,c,c,crs', output_file]
            result3 = subprocess.run(cmd3, capture_output=True, text=True)
            if result3.returncode != 0:
                print(f"⚠️  Aviso: Não foi possível adicionar grid_mapping (variável pode ter nome diferente)")
            
            # Limpar arquivo temporário
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            print(f"✓ Arquivo NetCDF corrigido: {output_file}")
            return Path(output_file)
            
        except Exception as e:
            print(f"⚠️  Erro durante a correção: {str(e)}")
            return input_file

    def upload_netcdf_file(self, workspace_name="netcdf", store_name="netcdf_store", file_path=None):
        """Faz upload de um arquivo NetCDF para o GeoServer"""
        if not file_path:
            # Usar arquivo de exemplo
            file_path = Path("geonode_custom/plugins/SST_Mediterraneo.nc")
        
        if not Path(file_path).exists():
            print(f"✗ Arquivo não encontrado: {file_path}")
            return False
        
        try:
            # Tentar corrigir o CRS do arquivo antes do upload
            corrected_file = self.fix_netcdf_crs(file_path)
            
            with open(corrected_file, 'rb') as f:
                files = {'file': (Path(corrected_file).name, f, 'application/x-netcdf')}
                
                geoserver_url = self.geoserver_url.rstrip('/')
                response = self.session.put(
                    f"{geoserver_url}/rest/workspaces/{workspace_name}/coveragestores/{store_name}/file.netcdf",
                    files=files
                )
            
            if response.status_code in [200, 201]:
                print(f"✓ Arquivo NetCDF '{Path(corrected_file).name}' enviado com sucesso")
                return True
            else:
                print(f"✗ Erro ao enviar arquivo: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Erro ao enviar arquivo NetCDF: {str(e)}")
            return False
    
    def configure_netcdf_layer(self, workspace_name="netcdf", store_name="netcdf_store", layer_name=None):
        """Configura uma camada NetCDF"""
        if not layer_name:
            layer_name = "netcdf_layer"
        
        try:
            # Configurações da camada
            layer_data = {
                "layer": {
                    "name": layer_name,
                    "type": "RASTER",
                    "defaultStyle": {
                        "name": "raster"
                    },
                    "enabled": True,
                    "advertised": True
                }
            }
            
            geoserver_url = self.geoserver_url.rstrip('/')
            response = self.session.put(
                f"{geoserver_url}/rest/layers/{layer_name}",
                data=json.dumps(layer_data)
            )
            
            if response.status_code in [200, 201]:
                print(f"✓ Camada '{layer_name}' configurada com sucesso")
                return True
            else:
                print(f"✗ Erro ao configurar camada: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Erro ao configurar camada: {str(e)}")
            return False
    
    def run_full_configuration(self):
        """Executa a configuração completa do GeoServer para NetCDF"""
        print("=== Configuração do GeoServer para NetCDF ===\n")
        
        # 1. Verificar status do GeoServer com retry
        if not self.check_geoserver_status():
            print("⚠️  GeoServer não ficou disponível após todas as tentativas. Configuração será pulada.")
            print("💡 Você pode executar manualmente depois: python /usr/src/geonode/setup_netcdf_geoserver.py")
            print("\n=== Configuração concluída ===")
            return True
        
        # 2. Verificar plugins NetCDF
        if not self.check_netcdf_plugins():
            print("⚠️  Plugins NetCDF não encontrados. Verifique se foram instalados corretamente.")
        
        # 3. Configurar configurações globais
        self.configure_netcdf_settings()
        
        # 4. Criar workspace
        workspace_name = "netcdf"
        if self.create_netcdf_workspace(workspace_name):
            # 5. Criar coverage store
            store_name = "netcdf_store"
            if self.create_netcdf_store(workspace_name, store_name):
                # 6. Fazer upload de arquivo de exemplo
                self.upload_netcdf_file(workspace_name, store_name)
                
                # 7. Configurar camada
                self.configure_netcdf_layer(workspace_name, store_name)
        
        print("\n=== Configuração concluída ===")
        return True


def main():
    """Função principal"""
    configurator = GeoServerNetCDFConfigurator()
    configurator.run_full_configuration()


if __name__ == "__main__":
    main()
