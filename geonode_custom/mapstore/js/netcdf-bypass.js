/**
 * NetCDF Bypass - Solução definitiva para validação frontend
 * Bypassa completamente a validação de tipos de arquivo para NetCDF
 */

(function() {
    'use strict';
    
    console.log('[NetCDF-Bypass] Iniciando bypass de validação...');
    
    // Função para interceptar e modificar validação de arquivos
    function bypassNetCDFValidation() {
        // Interceptar window.gn.validateFile se existir
        if (window.gn && window.gn.validateFile) {
            const originalValidateFile = window.gn.validateFile;
            window.gn.validateFile = function(file) {
                // Se for NetCDF, sempre retornar válido
                if (file && file.name && (file.name.endsWith('.nc') || file.name.endsWith('.netcdf'))) {
                    console.log('[NetCDF-Bypass] Arquivo NetCDF detectado:', file.name);
                    return {
                        valid: true,
                        type: 'netcdf',
                        errors: []
                    };
                }
                // Para outros arquivos, usar validação original
                return originalValidateFile.call(this, file);
            };
            console.log('[NetCDF-Bypass] validateFile interceptado');
        }
        
        // Interceptar validação de tipos suportados
        if (window.gn && window.gn.supportedFileTypes) {
            // Adicionar NetCDF aos tipos suportados
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
            console.log('[NetCDF-Bypass] NetCDF adicionado aos tipos suportados');
        }
        
        // Interceptar validação de extensões
        if (window.gn && window.gn.isValidFileType) {
            const originalIsValidFileType = window.gn.isValidFileType;
            window.gn.isValidFileType = function(file) {
                if (file && file.name && (file.name.endsWith('.nc') || file.name.endsWith('.netcdf'))) {
                    console.log('[NetCDF-Bypass] Tipo de arquivo NetCDF aceito:', file.name);
                    return true;
                }
                return originalIsValidFileType.call(this, file);
            };
            console.log('[NetCDF-Bypass] isValidFileType interceptado');
        }
        
        // Interceptar validação de arquivos ausentes
        if (window.gn && window.gn.checkMissingFiles) {
            const originalCheckMissingFiles = window.gn.checkMissingFiles;
            window.gn.checkMissingFiles = function(files) {
                // Se há arquivo NetCDF, não considerar como ausente
                const hasNetCDF = files && files.some(f => 
                    f.name && (f.name.endsWith('.nc') || f.name.endsWith('.netcdf'))
                );
                
                if (hasNetCDF) {
                    console.log('[NetCDF-Bypass] Arquivo NetCDF encontrado - bypassing missing files check');
                    return []; // Retorna lista vazia = nenhum arquivo ausente
                }
                
                return originalCheckMissingFiles.call(this, files);
            };
            console.log('[NetCDF-Bypass] checkMissingFiles interceptado');
        }
    }
    
    // Função para interceptar validação de upload
    function bypassUploadValidation() {
        // Interceptar validação de upload se existir
        if (window.gn && window.gn.validateUpload) {
            const originalValidateUpload = window.gn.validateUpload;
            window.gn.validateUpload = function(files) {
                // Se há NetCDF, sempre permitir upload
                const hasNetCDF = files && files.some(f => 
                    f.name && (f.name.endsWith('.nc') || f.name.endsWith('.netcdf'))
                );
                
                if (hasNetCDF) {
                    console.log('[NetCDF-Bypass] Upload NetCDF permitido');
                    return { valid: true, errors: [] };
                }
                
                return originalValidateUpload.call(this, files);
            };
            console.log('[NetCDF-Bypass] validateUpload interceptado');
        }
    }
    
    // Função para interceptar validação de tipos de arquivo
    function bypassFileTypeValidation() {
        // Interceptar validação de tipos se existir
        if (window.gn && window.gn.validateFileType) {
            const originalValidateFileType = window.gn.validateFileType;
            window.gn.validateFileType = function(file) {
                if (file && file.name && (file.name.endsWith('.nc') || file.name.endsWith('.netcdf'))) {
                    console.log('[NetCDF-Bypass] Tipo de arquivo NetCDF validado:', file.name);
                    return { valid: true, type: 'netcdf' };
                }
                return originalValidateFileType.call(this, file);
            };
            console.log('[NetCDF-Bypass] validateFileType interceptado');
        }
    }
    
    // Executar bypass quando DOM estiver pronto
    function initBypass() {
        console.log('[NetCDF-Bypass] Inicializando bypass...');
        
        bypassNetCDFValidation();
        bypassUploadValidation();
        bypassFileTypeValidation();
        
        console.log('[NetCDF-Bypass] Bypass inicializado com sucesso!');
    }
    
    // Executar imediatamente e também quando DOM estiver pronto
    initBypass();
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initBypass);
    }
    
    // Executar também após um delay para garantir que outros scripts carregaram
    setTimeout(initBypass, 1000);
    setTimeout(initBypass, 3000);
    
    console.log('[NetCDF-Bypass] Script carregado e executado');
})();




