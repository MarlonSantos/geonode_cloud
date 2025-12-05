/**
 * NetCDF Support Patch for GeoNode
 * Adds NetCDF file type support to the frontend validation
 */

// Wait for the document to be ready
(function() {
    'use strict';
    
    // Function to add NetCDF support
    function addNetCDFSupport() {
        // Add NetCDF to supported file types if the object exists
        if (window.gn && window.gn.supportedFileTypes) {
            // Add NetCDF configuration
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
            
            console.log('NetCDF support added to GeoNode');
        }
        
        // Override file validation function if it exists
        if (window.gn && window.gn.validateFile) {
            const originalValidateFile = window.gn.validateFile;
            window.gn.validateFile = function(file) {
                // Check if it's a NetCDF file
                if (file && file.name && (file.name.endsWith('.nc') || file.name.endsWith('.netcdf'))) {
                    return {
                        valid: true,
                        type: 'netcdf',
                        errors: []
                    };
                }
                // Fall back to original validation
                return originalValidateFile.call(this, file);
            };
        }
        
        // Patch missing files validation
        if (window.gn && window.gn.checkMissingFiles) {
            const originalCheckMissingFiles = window.gn.checkMissingFiles;
            window.gn.checkMissingFiles = function(files, type) {
                // NetCDF files don't need additional files
                if (type === 'netcdf') {
                    return [];
                }
                return originalCheckMissingFiles.call(this, files, type);
            };
        }
    }
    
    // Try to add support immediately
    addNetCDFSupport();
    
    // Also add when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', addNetCDFSupport);
    }
    
    // And try again after a short delay for dynamic content
    setTimeout(addNetCDFSupport, 1000);
    
})();
