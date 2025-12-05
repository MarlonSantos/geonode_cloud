/**
 * NetCDF Ultimate Bypass - Interceptação total
 * Este script intercepta TODAS as validações possíveis
 */

(function() {
    'use strict';
    
    console.log('[NetCDF-Ultimate] Iniciando bypass definitivo...');
    
    // Função para interceptar TODAS as validações possíveis
    function ultimateBypass() {
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
                        console.log('[NetCDF-Ultimate] Arquivo NetCDF aceito:', file.name);
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
                        console.log('[NetCDF-Ultimate] NetCDF - nenhum arquivo ausente');
                        return [];
                    }
                    return originalCheckMissingFiles.call(this, files, type);
                };
            }
            
            // Interceptar validateUpload
            if (window.gn.validateUpload) {
                const originalValidateUpload = window.gn.validateUpload;
                window.gn.validateUpload = function(files, type) {
                    const hasNetCDF = files && files.some(f =>
                        f.name && (f.name.endsWith('.nc') || f.name.endsWith('.netcdf'))
                    );
                    if (hasNetCDF) {
                        console.log('[NetCDF-Ultimate] validateUpload: NetCDF aceito');
                        return { valid: true, errors: [] };
                    }
                    return originalValidateUpload.call(this, files, type);
                };
            }
            
            // Interceptar isValidFileType
            if (window.gn.isValidFileType) {
                const originalIsValidFileType = window.gn.isValidFileType;
                window.gn.isValidFileType = function(file) {
                    if (file && file.name && (file.name.endsWith('.nc') || file.name.endsWith('.netcdf'))) {
                        console.log('[NetCDF-Ultimate] isValidFileType: NetCDF aceito');
                        return true;
                    }
                    return originalIsValidFileType.call(this, file);
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
            
            // Interceptar mensagens de erro
            if (window.gn.messages) {
                const originalMessages = window.gn.messages;
                window.gn.messages = function(key, params) {
                    if (key === 'missingFiles' && params && params.includes('netcdf')) {
                        console.log('[NetCDF-Ultimate] Interceptando mensagem missingFiles para NetCDF');
                        return 'NetCDF suportado - arquivos aceitos';
                    }
                    return originalMessages.call(this, key, params);
                };
            }
            
            console.log('[NetCDF-Ultimate] Bypass aplicado com sucesso');
        }
    }
    
    // Executar imediatamente
    ultimateBypass();
    
    // Executar quando DOM estiver pronto
    if (typeof document !== 'undefined') {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', ultimateBypass);
        } else {
            ultimateBypass();
        }
    }
    
    // Executar com delays para garantir interceptação
    setTimeout(ultimateBypass, 100);
    setTimeout(ultimateBypass, 500);
    setTimeout(ultimateBypass, 1000);
    setTimeout(ultimateBypass, 3000);
    setTimeout(ultimateBypass, 5000);
    
    // Interceptar também quando window.gn for definido
    if (typeof window !== 'undefined') {
        const originalGn = window.gn;
        Object.defineProperty(window, 'gn', {
            get: function() {
                const gn = originalGn || {};
                ultimateBypass();
                return gn;
            },
            set: function(value) {
                window._gn = value;
                ultimateBypass();
            }
        });
    }
    
})();




