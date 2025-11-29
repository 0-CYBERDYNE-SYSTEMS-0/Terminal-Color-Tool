function updateTerminalPreview(colors) {
     const container = document.getElementById('terminal-preview');
     if (!container) return;
     
     const bg = colors.background || '#1e1e1e';
     const fg = colors.foreground || '#d4d4d4';
     const cursor = colors.cursor || '#ffffff';
     
     container.innerHTML = `
         <div class="rounded-b-lg overflow-hidden" style="background-color: ${bg}">
             <!-- Terminal Header -->
             <div class="flex items-center gap-2 px-4 py-2 bg-gray-700/50">
                 <div class="w-3 h-3 rounded-full bg-red-500"></div>
                 <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
                 <div class="w-3 h-3 rounded-full bg-green-500"></div>
                 <span class="text-xs text-gray-400 ml-2">terminal</span>
             </div>
             
             <!-- Terminal Content -->
             <div class="p-4 text-sm font-mono leading-relaxed" style="color: ${fg}">
                 <div class="mb-2">
                     <span style="color: ${colors.green || '#0dbc79'}">user@theme-viz</span><span style="color: ${fg}">:</span><span style="color: ${colors.blue || '#2472c8'}">~</span><span style="color: ${fg}">$ </span><span>ls -la</span>
                 </div>
                 <div style="color: ${colors.bright_black || '#666666'}" class="mb-2">
                     total 48<br>
                     drwxr-xr-x 12 user user 4096 Nov 26 .<br>
                     drwxr-xr-x  4 user user 4096 Nov 20 ..
                 </div>
                 <div class="mb-2">
                     <span style="color: ${colors.yellow || '#e5e510'}">-rwxr-xr-x</span> 1 user user 352 Nov 26 <span style="color: ${colors.green || '#0dbc79'}">theme.py</span><br>
                     <span style="color: ${colors.cyan || '#11a8cd'}">-rw-r--r--</span> 1 user user 1244 Nov 26 <span style="color: ${colors.white || '#e5e5e5'}">README.md</span>
                 </div>
                 
                 <div class="mb-2">
                     <span style="color: ${colors.green || '#0dbc79'}">user@theme-viz</span><span style="color: ${fg}">:</span><span style="color: ${colors.blue || '#2472c8'}">~</span><span style="color: ${fg}">$ </span><span style="color: ${colors.magenta || '#bc3fbc'}">git status</span>
                 </div>
                 <div class="mb-2">
                     On branch <span style="color: ${colors.bright_green || '#23d18b'}">main</span><br>
                     <span style="color: ${colors.red || '#cd3131'}">Changes not staged:</span><br>
                     <span style="color: ${colors.bright_black || '#666666'}">&nbsp;&nbsp;modified:</span> <span style="color: ${colors.red || '#cd3131'}">app.py</span>
                 </div>
                 
                 <div class="mb-2">
                     <span style="color: ${colors.green || '#0dbc79'}">user@theme-viz</span><span style="color: ${fg}">:</span><span style="color: ${colors.blue || '#2472c8'}">~</span><span style="color: ${fg}">$ </span><span>echo "Hello World"</span>
                 </div>
                 <div class="mb-2" style="color: ${colors.bright_white || '#e5e5e5'}">Hello World</div>
                 
                 <div class="mb-2">
                     <span style="color: ${colors.green || '#0dbc79'}">user@theme-viz</span><span style="color: ${fg}">:</span><span style="color: ${colors.blue || '#2472c8'}">~</span><span style="color: ${fg}">$ </span><span style="color: ${colors.bright_yellow || '#f5f543'}">python3</span> --version
                 </div>
                 <div class="mb-2">Python <span style="color: ${colors.bright_cyan || '#29b8db'}">3.11.0</span></div>
                 
                 <div class="flex items-center">
                     <span style="color: ${colors.green || '#0dbc79'}">user@theme-viz</span><span style="color: ${fg}">:</span><span style="color: ${colors.blue || '#2472c8'}">~</span><span style="color: ${fg}">$ </span>
                     <span class="inline-block w-2 h-4 animate-pulse" style="background-color: ${cursor}"></span>
                 </div>
             </div>
         </div>
     `;
 }
