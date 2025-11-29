function showExportModal() {
     document.getElementById('export-modal').classList.remove('hidden');
 }
 
 function hideExportModal() {
     document.getElementById('export-modal').classList.add('hidden');
 }
 
 async function exportTheme() {
     const format = document.querySelector('input[name="export-format"]:checked').value;
     const themeName = document.getElementById('theme-name').value || 'My Theme';
     const colors = getCurrentColors();
     
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
         let filename = `${themeName.toLowerCase().replace(/\s+/g, '_')}.${format === 'json' || format === 'winterm' ? 'json' : format === 'iterm2' ? 'itermcolors' : format === 'xresources' ? 'Xresources' : 'sh'}`;
         
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
