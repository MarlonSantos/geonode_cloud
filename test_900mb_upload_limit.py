#!/usr/bin/env python3
"""
Script para testar o novo limite de upload de 900MB
"""

import os
import sys
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geonode.settings')
django.setup()

from django.conf import settings
from geonode.upload.models import UploadSizeLimit
from geonode.upload.utils import get_max_upload_size

def test_upload_limits():
    """Testa se os limites de upload estão configurados corretamente"""
    print("🔍 Testando configurações de limite de upload...")
    
    # 1. Verificar configuração no settings.py
    print(f"\n1. Configuração no settings.py:")
    default_max_size = getattr(settings, 'DEFAULT_MAX_UPLOAD_SIZE', None)
    if default_max_size:
        print(f"   ✓ DEFAULT_MAX_UPLOAD_SIZE: {default_max_size:,} bytes ({default_max_size / (1024*1024):.0f} MB)")
        if default_max_size == 943718400:  # 900MB
            print("   ✅ Configuração correta (900MB)")
        else:
            print(f"   ❌ Configuração incorreta. Esperado: 943,718,400 bytes (900MB)")
    else:
        print("   ❌ DEFAULT_MAX_UPLOAD_SIZE não encontrado")
    
    # 2. Verificar configurações de memória do Django
    print(f"\n2. Configurações de memória do Django:")
    file_upload_memory = getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', None)
    data_upload_memory = getattr(settings, 'DATA_UPLOAD_MAX_MEMORY_SIZE', None)
    
    if file_upload_memory:
        print(f"   ✓ FILE_UPLOAD_MAX_MEMORY_SIZE: {file_upload_memory:,} bytes ({file_upload_memory / (1024*1024):.0f} MB)")
    if data_upload_memory:
        print(f"   ✓ DATA_UPLOAD_MAX_MEMORY_SIZE: {data_upload_memory:,} bytes ({data_upload_memory / (1024*1024):.0f} MB)")
    
    # 3. Verificar limites no banco de dados
    print(f"\n3. Limites no banco de dados:")
    upload_slugs = [
        'dataset_upload_size',
        'document_upload_size',
        'netcdf_upload_size'
    ]
    
    for slug in upload_slugs:
        try:
            upload_limit = UploadSizeLimit.objects.get(slug=slug)
            size_mb = upload_limit.max_size / (1024*1024)
            print(f"   ✓ {slug}: {upload_limit.max_size:,} bytes ({size_mb:.0f} MB)")
            if upload_limit.max_size == 943718400:  # 900MB
                print(f"     ✅ Limite correto (900MB)")
            else:
                print(f"     ❌ Limite incorreto. Esperado: 900MB")
        except UploadSizeLimit.DoesNotExist:
            print(f"   ❌ {slug}: Não encontrado no banco de dados")
        except Exception as e:
            print(f"   ❌ {slug}: Erro ao consultar - {e}")
    
    # 4. Testar função get_max_upload_size
    print(f"\n4. Testando função get_max_upload_size:")
    try:
        max_size = get_max_upload_size('dataset_upload_size')
        size_mb = max_size / (1024*1024)
        print(f"   ✓ dataset_upload_size: {max_size:,} bytes ({size_mb:.0f} MB)")
        if max_size == 943718400:  # 900MB
            print("     ✅ Função retorna limite correto (900MB)")
        else:
            print(f"     ❌ Função retorna limite incorreto. Esperado: 900MB")
    except Exception as e:
        print(f"   ❌ Erro ao testar get_max_upload_size: {e}")
    
    # 5. Verificar variáveis de ambiente
    print(f"\n5. Variáveis de ambiente:")
    env_vars = [
        'DEFAULT_MAX_UPLOAD_SIZE',
        'FILE_UPLOAD_MAX_MEMORY_SIZE',
        'DATA_UPLOAD_MAX_MEMORY_SIZE'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            try:
                size_bytes = int(value)
                size_mb = size_bytes / (1024*1024)
                print(f"   ✓ {var}: {size_bytes:,} bytes ({size_mb:.0f} MB)")
            except ValueError:
                print(f"   ⚠️  {var}: {value} (não é um número)")
        else:
            print(f"   - {var}: Não definida")
    
    print(f"\n📋 Resumo:")
    print(f"   • Limite configurado: 900MB (943,718,400 bytes)")
    print(f"   • Configurações de memória: 50MB cada")
    print(f"   • Suporte a arquivos NetCDF até 900MB")
    print(f"   • Configuração do Nginx: client_max_body_size 900M")

def check_nginx_config():
    """Verifica se a configuração do Nginx está correta"""
    print(f"\n🌐 Verificando configuração do Nginx...")
    
    nginx_config_file = "nginx-upload-limit.conf"
    if os.path.exists(nginx_config_file):
        print(f"   ✓ Arquivo {nginx_config_file} encontrado")
        
        with open(nginx_config_file, 'r') as f:
            content = f.read()
            
        if "client_max_body_size 900M" in content:
            print("   ✅ Configuração do Nginx correta (900M)")
        else:
            print("   ❌ Configuração do Nginx incorreta")
            print("   Conteúdo atual:")
            print(content)
    else:
        print(f"   ❌ Arquivo {nginx_config_file} não encontrado")

if __name__ == '__main__':
    print("🚀 Teste do Limite de Upload de 900MB")
    print("=" * 50)
    
    test_upload_limits()
    check_nginx_config()
    
    print(f"\n✅ Teste concluído!")
    print(f"   Se todos os itens estão marcados com ✅, o limite de 900MB está configurado corretamente.")
    print(f"   Se há itens com ❌, execute o script update_upload_limits.py para corrigir.")

