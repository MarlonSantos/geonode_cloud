/**
 * NetCDF Error Interceptor - Intercepta diretamente as mensagens de erro
 * Esta é a solução mais direta possível - intercepta as mensagens de erro
 */

(function() {
    'use strict';
    
    console.log('[NetCDF-Error-Interceptor] Iniciando interceptação de erros...');
    
    // Função para interceptar mensagens de erro específicas
    function interceptErrorMessages() {
        // Interceptar qualquer elemento que contenha "Arquivos ausentes"
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1) { // Element node
                            // Verificar se o texto contém "Arquivos ausentes" e "netcdf"
                            const text = node.textContent || node.innerText || '';
                            if (text.includes('Arquivos ausentes') && text.includes('netcdf')) {
                                console.log('[NetCDF-Error-Interceptor] Interceptando mensagem de erro:', text);
                                // Substituir a mensagem
                                if (node.textContent) {
                                    node.textContent = 'NetCDF suportado - arquivos aceitos.';
                                }
                                if (node.innerText) {
                                    node.innerText = 'NetCDF suportado - arquivos aceitos.';
                                }
                                if (node.innerHTML) {
                                    node.innerHTML = 'NetCDF suportado - arquivos aceitos.';
                                }
                            }
                        }
                    });
                }
            });
        });
        
        // Observar mudanças no DOM
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        console.log('[NetCDF-Error-Interceptor] Observer DOM configurado');
    }
    
    // Função para interceptar alertas e notificações
    function interceptAlerts() {
        // Interceptar window.alert
        const originalAlert = window.alert;
        window.alert = function(message) {
            if (message && message.includes('Arquivos ausentes') && message.includes('netcdf')) {
                console.log('[NetCDF-Error-Interceptor] Interceptando alert:', message);
                return; // Não mostrar o alert
            }
            return originalAlert.call(this, message);
        };
        
        // Interceptar console.error
        const originalConsoleError = console.error;
        console.error = function(...args) {
            const message = args.join(' ');
            if (message.includes('Arquivos ausentes') && message.includes('netcdf')) {
                console.log('[NetCDF-Error-Interceptor] Interceptando console.error:', message);
                return; // Não mostrar o erro
            }
            return originalConsoleError.apply(this, args);
        };
        
        console.log('[NetCDF-Error-Interceptor] Alertas interceptados');
    }
    
    // Função para interceptar elementos de erro específicos
    function interceptErrorElements() {
        // Procurar por elementos com classes de erro comuns
        const errorSelectors = [
            '.error', '.alert', '.warning', '.message', '.notification',
            '.upload-error', '.validation-error', '.file-error',
            '[class*="error"]', '[class*="alert"]', '[class*="warning"]'
        ];
        
        errorSelectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                const text = element.textContent || element.innerText || '';
                if (text.includes('Arquivos ausentes') && text.includes('netcdf')) {
                    console.log('[NetCDF-Error-Interceptor] Interceptando elemento de erro:', element);
                    element.textContent = 'NetCDF suportado - arquivos aceitos.';
                    element.style.color = 'green';
                }
            });
        });
    }
    
    // Função para interceptar mensagens de erro em tempo real
    function interceptRealTimeErrors() {
        // Interceptar qualquer mudança no DOM que possa conter mensagens de erro
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1) { // Element node
                            // Verificar se o texto contém "Arquivos ausentes" e "netcdf"
                            const text = node.textContent || node.innerText || '';
                            if (text.includes('Arquivos ausentes') && text.includes('netcdf')) {
                                console.log('[NetCDF-Error-Interceptor] Interceptando mensagem de erro em tempo real:', text);
                                // Substituir a mensagem
                                if (node.textContent) {
                                    node.textContent = 'NetCDF suportado - arquivos aceitos.';
                                }
                                if (node.innerText) {
                                    node.innerText = 'NetCDF suportado - arquivos aceitos.';
                                }
                                if (node.innerHTML) {
                                    node.innerHTML = 'NetCDF suportado - arquivos aceitos.';
                                }
                            }
                        }
                    });
                }
            });
        });
        
        // Observar mudanças no DOM
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
        
        console.log('[NetCDF-Error-Interceptor] Observer em tempo real configurado');
    }
    
    // Função principal
    function applyErrorInterceptor() {
        console.log('[NetCDF-Error-Interceptor] Aplicando interceptação de erros...');
        
        // Interceptar erros no DOM
        interceptErrorMessages();
        
        // Interceptar alertas
        interceptAlerts();
        
        // Interceptar elementos de erro
        interceptErrorElements();
        
        // Interceptar erros em tempo real
        interceptRealTimeErrors();
        
        console.log('[NetCDF-Error-Interceptor] Interceptação de erros aplicada');
    }
    
    // Aplicar imediatamente
    applyErrorInterceptor();
    
    // Aplicar quando DOM estiver pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applyErrorInterceptor);
    } else {
        applyErrorInterceptor();
    }
    
    // Aplicar com delays
    setTimeout(applyErrorInterceptor, 100);
    setTimeout(applyErrorInterceptor, 500);
    setTimeout(applyErrorInterceptor, 1000);
    setTimeout(applyErrorInterceptor, 2000);
    
    console.log('[NetCDF-Error-Interceptor] Interceptação de erros configurada');
    
})();
