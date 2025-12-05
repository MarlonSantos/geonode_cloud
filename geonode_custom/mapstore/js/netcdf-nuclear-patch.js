/**
 * NetCDF Nuclear Patch - Modificação direta do MapStore
 * Este arquivo será injetado no gn-components.js compilado
 */

// NetCDF Nuclear Bypass - Executa imediatamente
(function() {
    'use strict';
    
    console.log('[NetCDF-Nuclear] Iniciando patch nuclear...');
    
    // Função para interceptar TODAS as validações
    function nuclearBypass() {
        // Interceptar window.gn se existir
        if (typeof window !== 'undefined') {
            if (!window.gn) {
                window.gn = {};
            }
            
            // Interceptar validateFile
            if (window.gn.validateFile) {
                const originalValidateFile = window.gn.validateFile;
                window.gn.validateFile = function(file) {
                    if (file && file.name && (file.name.endsWith('.nc') || file.name.endsWith('.netcdf'))) {
                        console.log('[NetCDF-Nuclear] Arquivo NetCDF aceito:', file.name);
                        return { valid: true, type: 'netcdf', errors: [] };
                    }
                    return originalValidateFile.call(this, file);
                };
            }
            
            // Interceptar checkMissingFiles
            if (window.gn.checkMissingFiles) {
                const originalCheckMissingFiles = window.gn.checkMissingFiles;
                window.gn.checkMissingFiles = function(files, type) {
                    if (type === 'netcdf' || (files && files.some(f => 
                        f.name && (f.name.endsWith('.nc') || f.name.endsWith('.netcdf'))
                    ))) {
                        console.log('[NetCDF-Nuclear] NetCDF - nenhum arquivo ausente');
                        return [];
                    }
                    return originalCheckMissingFiles.call(this, files, type);
                };
            }
            
            // Adicionar NetCDF aos tipos suportados
            if (!window.gn.supportedFileTypes) {
                window.gn.supportedFileTypes = {};
            }
            window.gn.supportedFileTypes.netcdf = {
                id: 'netcdf',
                label: 'NetCDF',
                formats: [{
                    label: 'NetCDF File',
                    required_ext: ['nc', 'netcdf'],
                    optional_ext: ['xml', 'sld']
                }],
                actions: ['upload', 'replace'],
                type: 'raster'
            };
            
            console.log('[NetCDF-Nuclear] Patch aplicado com sucesso');
        }
    }
    
    // Executar imediatamente
    nuclearBypass();
    
    // Executar quando DOM estiver pronto
    if (typeof document !== 'undefined') {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', nuclearBypass);
        } else {
            nuclearBypass();
        }
    }
    
    // Executar com delays para garantir interceptação
    setTimeout(nuclearBypass, 100);
    setTimeout(nuclearBypass, 500);
    setTimeout(nuclearBypass, 1000);
    setTimeout(nuclearBypass, 3000);
    
})();




