/**
 * DEBUG NetCDF - Script para investigar a validação real
 */

(function() {
    'use strict';
    
    console.log('=== DEBUG NetCDF - Investigando validação real ===');
    
    // 1. Verificar se window.gn existe
    console.log('window.gn existe:', typeof window !== 'undefined' && window.gn);
    
    if (typeof window !== 'undefined' && window.gn) {
        console.log('window.gn.supportedFileTypes:', window.gn.supportedFileTypes);
        console.log('window.gn.validateFile:', typeof window.gn.validateFile);
        console.log('window.gn.checkMissingFiles:', typeof window.gn.checkMissingFiles);
        console.log('window.gn.validateUpload:', typeof window.gn.validateUpload);
        console.log('window.gn.isValidFileType:', typeof window.gn.isValidFileType);
        
        // 2. Testar validação direta de um arquivo NetCDF
        const fakeNetCDFFile = {
            name: 'SST_Mediterraneo.nc',
            type: 'application/x-netcdf',
            size: 1024
        };
        
        console.log('=== TESTANDO VALIDAÇÕES ===');
        
        if (window.gn.validateFile) {
            try {
                const result = window.gn.validateFile(fakeNetCDFFile);
                console.log('validateFile result:', result);
            } catch (e) {
                console.log('validateFile error:', e);
            }
        }
        
        if (window.gn.checkMissingFiles) {
            try {
                const result = window.gn.checkMissingFiles([fakeNetCDFFile], 'netcdf');
                console.log('checkMissingFiles result:', result);
            } catch (e) {
                console.log('checkMissingFiles error:', e);
            }
        }
        
        if (window.gn.isValidFileType) {
            try {
                const result = window.gn.isValidFileType(fakeNetCDFFile);
                console.log('isValidFileType result:', result);
            } catch (e) {
                console.log('isValidFileType error:', e);
            }
        }
    }
    
    // 3. Verificar se há outras validações globais
    console.log('=== VERIFICANDO VALIDAÇÕES GLOBAIS ===');
    console.log('document.querySelector input[type=file]:', document.querySelector('input[type="file"]'));
    
    // 4. Interceptar TODAS as chamadas de função que podem estar validando
    const originalCall = Function.prototype.call;
    Function.prototype.call = function(...args) {
        if (args.length > 0 && typeof args[0] === 'object' && args[0] && args[0].name && args[0].name.includes('.nc')) {
            console.log('FUNÇÃO CHAMADA COM ARQUIVO .NC:', this.name, args);
        }
        return originalCall.apply(this, args);
    };
    
    console.log('=== DEBUG NetCDF - Setup completo ===');
})();
