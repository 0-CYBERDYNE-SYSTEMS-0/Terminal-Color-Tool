const COLOR_ORDER = [
     { key: 'background', label: 'Background' },
     { key: 'foreground', label: 'Foreground' },
     { key: 'cursor', label: 'Cursor' },
     { key: 'black', label: 'Black' },
     { key: 'red', label: 'Red' },
     { key: 'green', label: 'Green' },
     { key: 'yellow', label: 'Yellow' },
     { key: 'blue', label: 'Blue' },
     { key: 'magenta', label: 'Magenta' },
     { key: 'cyan', label: 'Cyan' },
     { key: 'white', label: 'White' },
     { key: 'bright_black', label: 'Bright Black' },
     { key: 'bright_red', label: 'Bright Red' },
     { key: 'bright_green', label: 'Bright Green' },
     { key: 'bright_yellow', label: 'Bright Yellow' },
     { key: 'bright_blue', label: 'Bright Blue' },
     { key: 'bright_magenta', label: 'Bright Magenta' },
     { key: 'bright_cyan', label: 'Bright Cyan' },
     { key: 'bright_white', label: 'Bright White' },
 ];
 
 const DEFAULT_COLORS = {
     background: '#1e1e1e',
     foreground: '#d4d4d4',
     cursor: '#ffffff',
     black: '#000000',
     red: '#cd3131',
     green: '#0dbc79',
     yellow: '#e5e510',
     blue: '#2472c8',
     magenta: '#bc3fbc',
     cyan: '#11a8cd',
     white: '#e5e5e5',
     bright_black: '#666666',
     bright_red: '#f14c4c',
     bright_green: '#23d18b',
     bright_yellow: '#f5f543',
     bright_blue: '#3b8eea',
     bright_magenta: '#d670d6',
     bright_cyan: '#29b8db',
     bright_white: '#e5e5e5',
 };
 
 let currentColors = { ...DEFAULT_COLORS };
 let onColorChange = null;
 
 function hexToRgb(hex) {
     const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
     return result ? {
         r: parseInt(result[1], 16),
         g: parseInt(result[2], 16),
         b: parseInt(result[3], 16)
     } : { r: 0, g: 0, b: 0 };
 }
 
 function rgbToHex(r, g, b) {
     return '#' + [r, g, b].map(x => {
         const hex = Math.round(x).toString(16);
         return hex.length === 1 ? '0' + hex : hex;
     }).join('');
 }
 
 function createColorRow(colorKey, label) {
     const rgb = hexToRgb(currentColors[colorKey]);
     
     const row = document.createElement('div');
     row.className = 'color-row bg-gray-700/50 rounded p-3';
     row.innerHTML = `
         <div class="flex items-center gap-3 mb-2">
             <div class="color-swatch w-8 h-8 rounded border border-gray-600" 
                  style="background-color: ${currentColors[colorKey]}" 
                  data-color="${colorKey}"></div>
             <span class="text-sm font-medium flex-1">${label}</span>
             <input type="text" value="${currentColors[colorKey].toUpperCase()}" 
                    class="hex-input w-20 bg-gray-800 border border-gray-600 rounded px-2 py-1 text-xs font-mono text-center focus:outline-none focus:border-blue-500"
                    data-color="${colorKey}">
         </div>
         <div class="slider-container space-y-1">
             <div class="flex items-center gap-2">
                 <span class="text-xs text-red-400 w-4">R</span>
                 <input type="range" min="0" max="255" value="${rgb.r}" 
                        class="slider-r flex-1" data-color="${colorKey}" data-channel="r">
                 <span class="text-xs text-gray-400 w-8 text-right" data-value="${colorKey}-r">${rgb.r}</span>
             </div>
             <div class="flex items-center gap-2">
                 <span class="text-xs text-green-400 w-4">G</span>
                 <input type="range" min="0" max="255" value="${rgb.g}" 
                        class="slider-g flex-1" data-color="${colorKey}" data-channel="g">
                 <span class="text-xs text-gray-400 w-8 text-right" data-value="${colorKey}-g">${rgb.g}</span>
             </div>
             <div class="flex items-center gap-2">
                 <span class="text-xs text-blue-400 w-4">B</span>
                 <input type="range" min="0" max="255" value="${rgb.b}" 
                        class="slider-b flex-1" data-color="${colorKey}" data-channel="b">
                 <span class="text-xs text-gray-400 w-8 text-right" data-value="${colorKey}-b">${rgb.b}</span>
             </div>
         </div>
     `;
     
     row.querySelectorAll('input[type="range"]').forEach(slider => {
         slider.addEventListener('input', handleSliderChange);
     });
     
     row.querySelector('.hex-input').addEventListener('change', handleHexChange);
     row.querySelector('.hex-input').addEventListener('keydown', (e) => {
         if (e.key === 'Enter') handleHexChange(e);
     });
     
     return row;
 }
 
 function handleSliderChange(e) {
     const colorKey = e.target.dataset.color;
     const channel = e.target.dataset.channel;
     const value = parseInt(e.target.value);
     
     const rgb = hexToRgb(currentColors[colorKey]);
     rgb[channel] = value;
     
     const newHex = rgbToHex(rgb.r, rgb.g, rgb.b);
     updateColor(colorKey, newHex);
 }
 
 function handleHexChange(e) {
     const colorKey = e.target.dataset.color;
     let value = e.target.value.trim();
     
     if (!value.startsWith('#')) value = '#' + value;
     if (/^#[0-9A-Fa-f]{6}$/.test(value)) {
         updateColor(colorKey, value.toLowerCase());
     } else {
         e.target.value = currentColors[colorKey].toUpperCase();
     }
 }
 
 function updateColor(colorKey, hexValue) {
     currentColors[colorKey] = hexValue;
     const rgb = hexToRgb(hexValue);
     
     const swatch = document.querySelector(`.color-swatch[data-color="${colorKey}"]`);
     if (swatch) swatch.style.backgroundColor = hexValue;
     
     const hexInput = document.querySelector(`.hex-input[data-color="${colorKey}"]`);
     if (hexInput) hexInput.value = hexValue.toUpperCase();
     
     ['r', 'g', 'b'].forEach(ch => {
         const slider = document.querySelector(`input[type="range"][data-color="${colorKey}"][data-channel="${ch}"]`);
         if (slider) slider.value = rgb[ch];
         
         const valueLabel = document.querySelector(`[data-value="${colorKey}-${ch}"]`);
         if (valueLabel) valueLabel.textContent = rgb[ch];
     });
     
     if (onColorChange) onColorChange(currentColors);
 }
 
 function updateAllColors(newColors) {
     Object.assign(currentColors, newColors);
     
     COLOR_ORDER.forEach(({ key }) => {
         if (newColors[key]) {
             const rgb = hexToRgb(newColors[key]);
             
             const swatch = document.querySelector(`.color-swatch[data-color="${key}"]`);
             if (swatch) swatch.style.backgroundColor = newColors[key];
             
             const hexInput = document.querySelector(`.hex-input[data-color="${key}"]`);
             if (hexInput) hexInput.value = newColors[key].toUpperCase();
             
             ['r', 'g', 'b'].forEach(ch => {
                 const slider = document.querySelector(`input[type="range"][data-color="${key}"][data-channel="${ch}"]`);
                 if (slider) slider.value = rgb[ch];
                 
                 const valueLabel = document.querySelector(`[data-value="${key}-${ch}"]`);
                 if (valueLabel) valueLabel.textContent = rgb[ch];
             });
         }
     });
     
     if (onColorChange) onColorChange(currentColors);
 }
 
 function initColorPicker(container, callback) {
     onColorChange = callback;
     container.innerHTML = '';
     
     COLOR_ORDER.forEach(({ key, label }) => {
         container.appendChild(createColorRow(key, label));
     });
     
     if (callback) callback(currentColors);
 }
 
 function getCurrentColors() {
     return { ...currentColors };
 }
