const THEME_PRESETS = {
     "Tokyo Night": {
         background: '#1a1b26', foreground: '#a9b1d6', cursor: '#ffffff',
         black: '#1a1b26', red: '#f7768e', green: '#9ece6a', yellow: '#e0af68',
         blue: '#7aa2f7', magenta: '#bb9af7', cyan: '#7dcfff', white: '#a9b1d6',
         bright_black: '#414868', bright_red: '#f7768e', bright_green: '#9ece6a',
         bright_yellow: '#e0af68', bright_blue: '#7aa2f7', bright_magenta: '#bb9af7',
         bright_cyan: '#7dcfff', bright_white: '#c0caf5'
     },
     "Solarized Dark": {
         background: '#002b36', foreground: '#839496', cursor: '#ffffff',
         black: '#073642', red: '#dc322f', green: '#859900', yellow: '#b58900',
         blue: '#268bd2', magenta: '#d33682', cyan: '#2aa198', white: '#eee8d5',
         bright_black: '#002b36', bright_red: '#cb4b16', bright_green: '#586e75',
         bright_yellow: '#657b83', bright_blue: '#839496', bright_magenta: '#6c71c4',
         bright_cyan: '#93a1a1', bright_white: '#fdf6e3'
     },
     "Dracula": {
         background: '#282a36', foreground: '#f8f8f2', cursor: '#f8f8f2',
         black: '#21222c', red: '#ff5555', green: '#50fa7b', yellow: '#f1fa8c',
         blue: '#bd93f9', magenta: '#ff79c6', cyan: '#8be9fd', white: '#f8f8f2',
         bright_black: '#6272a4', bright_red: '#ff6e6e', bright_green: '#69ff94',
         bright_yellow: '#ffffa5', bright_blue: '#d6acff', bright_magenta: '#ff92df',
         bright_cyan: '#a4ffff', bright_white: '#ffffff'
     },
     "Monokai": {
         background: '#272822', foreground: '#f8f8f2', cursor: '#f8f8f2',
         black: '#272822', red: '#f92672', green: '#a6e22e', yellow: '#f4bf75',
         blue: '#66d9ef', magenta: '#ae81ff', cyan: '#a1efe4', white: '#f8f8f2',
         bright_black: '#75715e', bright_red: '#f92672', bright_green: '#a6e22e',
         bright_yellow: '#f4bf75', bright_blue: '#66d9ef', bright_magenta: '#ae81ff',
         bright_cyan: '#a1efe4', bright_white: '#f9f8f5'
     },
     "Nord": {
         background: '#2e3440', foreground: '#d8dee9', cursor: '#d8dee9',
         black: '#3b4252', red: '#bf616a', green: '#a3be8c', yellow: '#ebcb8b',
         blue: '#81a1c1', magenta: '#b48ead', cyan: '#88c0d0', white: '#e5e9f0',
         bright_black: '#4c566a', bright_red: '#bf616a', bright_green: '#a3be8c',
         bright_yellow: '#ebcb8b', bright_blue: '#81a1c1', bright_magenta: '#b48ead',
         bright_cyan: '#8fbcbb', bright_white: '#eceff4'
     },
     "Gruvbox": {
         background: '#282828', foreground: '#ebdbb2', cursor: '#ebdbb2',
         black: '#282828', red: '#cc241d', green: '#98971a', yellow: '#d79921',
         blue: '#458588', magenta: '#b16286', cyan: '#689d6a', white: '#a89984',
         bright_black: '#928374', bright_red: '#fb4934', bright_green: '#b8bb26',
         bright_yellow: '#fabd2f', bright_blue: '#83a598', bright_magenta: '#d3869b',
         bright_cyan: '#8ec07c', bright_white: '#ebdbb2'
     },
     "One Dark": {
         background: '#282c34', foreground: '#abb2bf', cursor: '#528bff',
         black: '#282c34', red: '#e06c75', green: '#98c379', yellow: '#e5c07b',
         blue: '#61afef', magenta: '#c678dd', cyan: '#56b6c2', white: '#abb2bf',
         bright_black: '#5c6370', bright_red: '#e06c75', bright_green: '#98c379',
         bright_yellow: '#e5c07b', bright_blue: '#61afef', bright_magenta: '#c678dd',
         bright_cyan: '#56b6c2', bright_white: '#ffffff'
     }
 };
 
 function createPresetButtons() {
     const container = document.getElementById('presets-container');
     if (!container) return;
     
     Object.entries(THEME_PRESETS).forEach(([name, colors]) => {
         const btn = document.createElement('button');
         btn.className = 'w-full flex items-center gap-3 p-2 bg-gray-700 hover:bg-gray-600 rounded transition text-left';
         btn.innerHTML = `
             <div class="flex gap-0.5">
                 <div class="w-3 h-6 rounded-l" style="background-color: ${colors.background}"></div>
                 <div class="w-3 h-6" style="background-color: ${colors.red}"></div>
                 <div class="w-3 h-6" style="background-color: ${colors.green}"></div>
                 <div class="w-3 h-6" style="background-color: ${colors.blue}"></div>
                 <div class="w-3 h-6 rounded-r" style="background-color: ${colors.foreground}"></div>
             </div>
             <span class="text-sm">${name}</span>
         `;
         btn.addEventListener('click', () => {
             updateAllColors(colors);
             document.getElementById('theme-name').value = name;
         });
         container.appendChild(btn);
     });
 }
 
 function setupImageUpload() {
     const dropZone = document.getElementById('drop-zone');
     const fileInput = document.getElementById('file-input');
     const extractBtn = document.getElementById('extract-btn');
     const previewImg = document.getElementById('preview-image');
     const dropContent = document.getElementById('drop-content');
     
     let selectedFile = null;
     
     dropZone.addEventListener('click', () => fileInput.click());
     
     dropZone.addEventListener('dragover', (e) => {
         e.preventDefault();
         dropZone.classList.add('dragover');
     });
     
     dropZone.addEventListener('dragleave', () => {
         dropZone.classList.remove('dragover');
     });
     
     dropZone.addEventListener('drop', (e) => {
         e.preventDefault();
         dropZone.classList.remove('dragover');
         const file = e.dataTransfer.files[0];
         if (file && file.type.startsWith('image/')) {
             handleFile(file);
         }
     });
     
     fileInput.addEventListener('change', (e) => {
         if (e.target.files[0]) {
             handleFile(e.target.files[0]);
         }
     });
     
     function handleFile(file) {
         selectedFile = file;
         const reader = new FileReader();
         reader.onload = (e) => {
             previewImg.src = e.target.result;
             previewImg.classList.remove('hidden');
             dropContent.classList.add('hidden');
         };
         reader.readAsDataURL(file);
         extractBtn.disabled = false;
     }
     
     extractBtn.addEventListener('click', async () => {
         if (!selectedFile) return;
         
         extractBtn.disabled = true;
         extractBtn.textContent = 'Extracting...';
         
         const formData = new FormData();
         formData.append('image', selectedFile);
         
         try {
             const response = await fetch('/api/extract-colors', {
                 method: 'POST',
                 body: formData
             });
             
             if (!response.ok) throw new Error('Extraction failed');
             
             const data = await response.json();
             updateAllColors(data.colors);
             document.getElementById('theme-name').value = 'Extracted Theme';
         } catch (error) {
             console.error('Extraction error:', error);
             alert('Failed to extract colors. Please try another image.');
         } finally {
             extractBtn.disabled = false;
             extractBtn.textContent = 'Extract Colors';
         }
     });
 }
 
 document.addEventListener('DOMContentLoaded', () => {
     const colorPickerContainer = document.getElementById('color-picker');
     
     initColorPicker(colorPickerContainer, (colors) => {
         updateTerminalPreview(colors);
     });
     
     createPresetButtons();
     setupImageUpload();
 });
