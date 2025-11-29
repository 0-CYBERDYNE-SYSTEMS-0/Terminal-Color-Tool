function showExportModal() {
     document.getElementById('export-modal').classList.remove('hidden');
     updateWeztermCheckboxVisibility();
 }
 
 function hideExportModal() {
     document.getElementById('export-modal').classList.add('hidden');
 }
 
 function updateWeztermCheckboxVisibility() {
     const selectedFormat = document.querySelector('input[name="export-format"]:checked').value;
     const checkboxContainer = document.getElementById('auto-install-wezterm').closest('.bg-gray-700');
     
     if (selectedFormat === 'wezterm') {
         checkboxContainer.style.display = 'block';
     } else {
         checkboxContainer.style.display = 'none';
         document.getElementById('auto-install-wezterm').checked = false;
     }
 }
 
 // Add event listeners to radio buttons to toggle checkbox visibility
 document.addEventListener('DOMContentLoaded', function() {
     const radioButtons = document.querySelectorAll('input[name="export-format"]');
     radioButtons.forEach(radio => {
         radio.addEventListener('change', updateWeztermCheckboxVisibility);
     });
     // Initial visibility check
     updateWeztermCheckboxVisibility();
 });
 
 async function exportTheme() {
     const format = document.querySelector('input[name="export-format"]:checked').value;
     const themeName = document.getElementById('theme-name').value || 'My Theme';
     const colors = getCurrentColors();
     const autoInstall = document.getElementById('auto-install-wezterm').checked;
     
     // Handle WezTerm auto-install
     if (format === 'wezterm' && autoInstall) {
         try {
             const response = await fetch('/api/install-wezterm', {
                 method: 'POST',
                 headers: { 'Content-Type': 'application/json' },
                 body: JSON.stringify({
                     theme_name: themeName,
                     colors: colors
                 })
             });
             
             if (!response.ok) {
                 const errorData = await response.json();
                 throw new Error(errorData.detail || 'Installation failed');
             }
             
             const result = await response.json();
             
             // Show success message with instructions
             alert(`${result.message}\n\n${result.instructions}\n\nConfig file: ${result.config_path}`);
             hideExportModal();
             return;
         } catch (error) {
             console.error('Installation error:', error);
             alert(`Failed to install theme: ${error.message}\n\nYou can still download the theme manually.`);
             // Fall through to regular download
         }
     }
     
     // Regular download for all formats
     try {
         const response = await fetch('/api/export', {
             method: 'POST',
             headers: { 'Content-Type': 'application/json' },
             body: JSON.stringify({
                 format: format,
                 theme_data: { name: themeName, colors: colors }
             })
         });
         
         if (!response.ok) {
             throw new Error('Export failed');
         }
         
         const blob = await response.blob();
         const contentDisposition = response.headers.get('Content-Disposition');
         let filename = `${themeName.toLowerCase().replace(/\s+/g, '_')}.${format === 'json' || format === 'winterm' || format === 'wezterm' ? format === 'wezterm' ? 'lua' : 'json' : format === 'iterm2' ? 'itermcolors' : format === 'xresources' ? 'Xresources' : 'sh'}`;
         
         if (contentDisposition) {
             const match = contentDisposition.match(/filename="(.+)"/);
             if (match) filename = match[1];
         }
         
         const url = URL.createObjectURL(blob);
         const a = document.createElement('a');
         a.href = url;
         a.download = filename;
         document.body.appendChild(a);
         a.click();
         document.body.removeChild(a);
         URL.revokeObjectURL(url);
         
         hideExportModal();
     } catch (error) {
         console.error('Export error:', error);
         alert('Failed to export theme. Please try again.');
     }
 }
 
 document.getElementById('export-modal').addEventListener('click', (e) => {
     if (e.target.id === 'export-modal') hideExportModal();
 });
