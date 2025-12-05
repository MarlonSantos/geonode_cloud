#!/usr/bin/env python3
"""
Script para atualizar os limites de upload no banco de dados do GeoNode
Este script deve ser executado após as mudanças nas configurações para atualizar
os registros existentes no banco de dados.
"""

import os
import sys
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geonode.settings')
django.setup()

from geonode.upload.models import UploadSizeLimit
from django.conf import settings

def update_upload_limits():
    """Atualiza os limites de upload no banco de dados"""
    
    # Novo limite: 900 MB
    new_limit = 943718400  # 900 MB em bytes
    
    print(f"Atualizando limites de upload para {new_limit / (1024*1024):.0f} MB...")
    
    # Lista de slugs que precisam ser atualizados
    upload_slugs = [
        'dataset_upload_size',
        'document_upload_size',
        'netcdf_upload_size'
    ]
    
    updated_count = 0
    
    for slug in upload_slugs:
        try:
            # Buscar ou criar o limite
            upload_limit, created = UploadSizeLimit.objects.get_or_create(
                slug=slug,
                defaults={
                    'description': f'Maximum file size for {slug}',
                    'max_size': new_limit
                }
            )
            
            if not created:
                # Atualizar o limite existente
                old_size = upload_limit.max_size
                upload_limit.max_size = new_limit
                upload_limit.save()
                print(f"✓ Atualizado {slug}: {old_size / (1024*1024):.0f} MB → {new_limit / (1024*1024):.0f} MB")
            else:
                print(f"✓ Criado novo limite para {slug}: {new_limit / (1024*1024):.0f} MB")
            
            updated_count += 1
            
        except Exception as e:
            print(f"✗ Erro ao atualizar {slug}: {e}")
    
    print(f"\nResumo: {updated_count} limites atualizados com sucesso!")
    print(f"Novo limite de upload: {new_limit / (1024*1024):.0f} MB")

if __name__ == '__main__':
    update_upload_limits()
