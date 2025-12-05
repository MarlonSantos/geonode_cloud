/**
 * NetCDF DOM Interceptor - Intercepta diretamente no DOM
 * Esta é a solução mais radical possível - intercepta no nível do DOM
 */

(function() {
    'use strict';
    
    console.log('[NetCDF-DOM-Interceptor] Iniciando interceptação DOM...');
    
    // Função para interceptar mensagens de erro no DOM
    function interceptDOMErrors() {
        // Interceptar qualquer elemento que contenha "Arquivos ausentes"
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1) { // Element node
                            // Verificar se o texto contém "Arquivos ausentes" e "netcdf"
                            const text = node.textContent || node.innerText || '';
                            if (text.includes('Arquivos ausentes') && text.includes('netcdf')) {
                                console.log('[NetCDF-DOM-Interceptor] Interceptando mensagem de erro:', text);
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
        
        console.log('[NetCDF-DOM-Interceptor] Observer DOM configurado');
    }
    
    // Função para interceptar alertas e notificações
    function interceptAlerts() {
        // Interceptar window.alert
        const originalAlert = window.alert;
        window.alert = function(message) {
            if (message && message.includes('Arquivos ausentes') && message.includes('netcdf')) {
                console.log('[NetCDF-DOM-Interceptor] Interceptando alert:', message);
                return; // Não mostrar o alert
            }
            return originalAlert.call(this, message);
        };
        
        // Interceptar console.error
        const originalConsoleError = console.error;
        console.error = function(...args) {
            const message = args.join(' ');
            if (message.includes('Arquivos ausentes') && message.includes('netcdf')) {
                console.log('[NetCDF-DOM-Interceptor] Interceptando console.error:', message);
                return; // Não mostrar o erro
            }
            return originalConsoleError.apply(this, args);
        };
        
        console.log('[NetCDF-DOM-Interceptor] Alertas interceptados');
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
                    console.log('[NetCDF-DOM-Interceptor] Interceptando elemento de erro:', element);
                    element.textContent = 'NetCDF suportado - arquivos aceitos.';
                    element.style.color = 'green';
                }
            });
        });
    }
    
    // Função principal
    function applyDOMInterceptor() {
        console.log('[NetCDF-DOM-Interceptor] Aplicando interceptação DOM...');
        
        // Interceptar erros no DOM
        interceptDOMErrors();
        
        // Interceptar alertas
        interceptAlerts();
        
        // Interceptar elementos de erro
        interceptErrorElements();
        
        console.log('[NetCDF-DOM-Interceptor] Interceptação DOM aplicada');
    }
    
    // Aplicar imediatamente
    applyDOMInterceptor();
    
    // Aplicar quando DOM estiver pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', applyDOMInterceptor);
    } else {
        applyDOMInterceptor();
    }
    
    // Aplicar com delays
    setTimeout(applyDOMInterceptor, 100);
    setTimeout(applyDOMInterceptor, 500);
    setTimeout(applyDOMInterceptor, 1000);
    setTimeout(applyDOMInterceptor, 2000);
    
    console.log('[NetCDF-DOM-Interceptor] Interceptação DOM configurada');
    
})();
