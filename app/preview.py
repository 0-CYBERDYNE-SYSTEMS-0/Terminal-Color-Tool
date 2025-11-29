"""
Terminal Preview Panel for the Theme Creator

This module provides a real-time preview of how the theme would look in a terminal.
"""

import tkinter as tk
from tkinter import ttk, font


class PreviewPanel(tk.Frame):
    """Widget for previewing the terminal color theme."""
    
    def __init__(self, parent, initial_colors):
        super().__init__(parent)
        self.colors = initial_colors.copy()
        self.setup_ui()
        
    def setup_ui(self):
        """Create the terminal preview UI components."""
        # Create terminal-like frame
        terminal_frame = tk.Frame(self, bg=self.colors['background'], relief=tk.SUNKEN, borderwidth=2)
        terminal_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create terminal header
        header_frame = tk.Frame(terminal_frame, bg='#333333', height=30)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Terminal buttons
        for i, color in enumerate(['#ff5f56', '#ffbd2e', '#27c93f']):
            btn = tk.Frame(header_frame, bg=color, width=15, height=20, relief=tk.RAISED, borderwidth=1)
            btn.place(x=10 + i * 25, y=5)
            btn.pack_propagate(False)
        
        # Terminal title
        title_label = tk.Label(header_frame, text="terminal", bg='#333333', fg='white', font=('Arial', 9))
        title_label.place(x=80, y=5)
        
        # Create terminal content area with scrollbar
        content_frame = tk.Frame(terminal_frame, bg=self.colors['background'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(content_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create text widget for terminal content
        self.terminal_text = tk.Text(
            content_frame,
            bg=self.colors['background'],
            fg=self.colors['foreground'],
            font=('Consolas', '10'),
            insertbackground=self.colors['cursor'],
            selectbackground=self.colors['cursor'],
            relief=tk.FLAT,
            wrap=tk.NONE,
            yscrollcommand=scrollbar.set
        )
        self.terminal_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.terminal_text.yview)
        
        # Disable text editing
        self.terminal_text.bind('<Key>', lambda e: 'break')
        self.terminal_text.bind('<Button-1>', lambda e: 'break')
        
        # Populate with sample terminal content
        self.populate_terminal_content()
        
    def populate_terminal_content(self):
        """Fill the terminal preview with sample content."""
        # Clear existing content
        self.terminal_text.delete(1.0, tk.END)
        
        # Set up tags for different colors
        self.terminal_text.tag_config('normal', foreground=self.colors['foreground'])
        self.terminal_text.tag_config('black', foreground=self.colors['black'])
        self.terminal_text.tag_config('red', foreground=self.colors['red'])
        self.terminal_text.tag_config('green', foreground=self.colors['green'])
        self.terminal_text.tag_config('yellow', foreground=self.colors['yellow'])
        self.terminal_text.tag_config('blue', foreground=self.colors['blue'])
        self.terminal_text.tag_config('magenta', foreground=self.colors['magenta'])
        self.terminal_text.tag_config('cyan', foreground=self.colors['cyan'])
        self.terminal_text.tag_config('white', foreground=self.colors['white'])
        self.terminal_text.tag_config('bright_black', foreground=self.colors['bright_black'])
        self.terminal_text.tag_config('bright_red', foreground=self.colors['bright_red'])
        self.terminal_text.tag_config('bright_green', foreground=self.colors['bright_green'])
        self.terminal_text.tag_config('bright_yellow', foreground=self.colors['bright_yellow'])
        self.terminal_text.tag_config('bright_blue', foreground=self.colors['bright_blue'])
        self.terminal_text.tag_config('bright_magenta', foreground=self.colors['bright_magenta'])
        self.terminal_text.tag_config('bright_cyan', foreground=self.colors['bright_cyan'])
        self.terminal_text.tag_config('bright_white', foreground=self.colors['bright_white'])
        self.terminal_text.tag_config('cursor', background=self.colors['cursor'])
        
        # Sample terminal content
        content = """╔═══════════════════════════════════════════════════════════════╗
║                     Welcome to Theme Viz                      ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║ <span style="color:{red}">user@theme-viz</span>:~$ <span style="color:green">ls -la</span>                                               ║
║                                                               ║
║ total 48                                                      ║
║ drwxr-xr-x 12 user user 4096 Nov 26 09:26 .                   ║
║ drwxr-xr-x  4 user user 4096 Nov 20 15:27 ..                  ║
║ -rw-r--r--  1 user user  220 Nov 20 15:27 .bash_logout        ║
║ -rw-r--r--  1 user user 3771 Nov 20 15:27 .bashrc            ║
║ -rw-r--r--  1 user user  807 Nov 20 15:27 .profile           ║
║ -rwxr-xr-x  1 user user  352 Nov 26 09:25 <span style="color:yellow">theme_generator.py</span>                            ║
║ -rw-r--r--  1 user user 1244 Nov 26 09:26 <span style="color:cyan">README.md</span>                                     ║
║                                                               ║
║ <span style="color:{red}">user@theme-viz</span>:~$ <span style="color:green">cat README.md</span>                                              ║
║                                                               ║
║ # Terminal Color Theme Creator                                ║
║                                                               ║
║ A simple, intuitive application for creating and exporting    ║
║ terminal color themes.                                        ║
║                                                               ║
║ Features:                                                     ║
║ • Extract colors from images                                  ║
║ • Interactive color sliders                                   ║
║ • Real-time preview                                           ║
║ • Export to multiple formats                                  ║
║                                                               ║
║ <span style="color:{red}">user@theme-viz</span>:~$ <span style="color:green">echo $SHELL</span>                                              ║
║ /bin/bash                                                     ║
║                                                               ║
║ <span style="color:{red}">user@theme-viz</span>:~$ <span style="color:magenta">git status</span>                                             ║
║ On branch main                                                ║
║                                                               ║
║ No commits yet                                                 ║
║                                                               ║
║ Untracked files:                                              ║
║   (use "git add <file>..." to include in what will be committed)║
║                                                               ║
║       <span style="color:red">theme_generator.py</span>                                          ║
║       <span style="color:red">README.md</span>                                               ║
║                                                               ║
║ <span style="color:{red}">user@theme-viz</span>:~$ <span style="color:green">date</span>                                                   ║
║ Wed Nov 26 09:26:31 PST 2024                                  ║
║                                                               ║
║ <span style="color:{red}">user@theme-viz</span>:~$ <span style="color:green">ls --color=always</span>                                        ║
║ total 48                                                      ║
║ drwxr-xr-x 12 user user 4096 Nov 26 09:26 <span style="color:blue">.</span>                   ║
║ drwxr-xr-x  4 user user 4096 Nov 20 15:27 <span style="color:blue">..</span>                  ║
║ -rw-r--r--  1 user user  220 Nov 20 15:27 <span style="color:blue">.bash_logout</span>        ║
║ -rw-r--r--  1 user user 3771 Nov 20 15:27 <span style="color:blue">.bashrc</span>            ║
║ -rw-r--r--  1 user user  807 Nov 20 15:27 <span style="color:blue">.profile</span>           ║
║ -rwxr-xr-x  1 user user  352 Nov 26 09:25 <span style="color:yellow">theme_generator.py</span>                            ║
║ -rw-r--r--  1 user user 1244 Nov 26 09:26 <span style="color:cyan">README.md</span>                                     ║
║                                                               ║
║ <span style="color:{red}">user@theme-viz</span>:~$ <span style="color:green">python3 theme_generator.py</span>                                    ║
╚═══════════════════════════════════════════════════════════════╝
""".format(
            red=self.colors['red'],
            green=self.colors['green'],
            yellow=self.colors['yellow'],
            blue=self.colors['blue'],
            magenta=self.colors['magenta'],
            cyan=self.colors['cyan'],
            white=self.colors['white'],
            bright_black=self.colors['bright_black'],
            bright_red=self.colors['bright_red'],
            bright_green=self.colors['bright_green'],
            bright_yellow=self.colors['bright_yellow'],
            bright_blue=self.colors['bright_blue'],
            bright_magenta=self.colors['bright_magenta'],
            bright_cyan=self.colors['bright_cyan'],
            bright_white=self.colors['bright_white']
        )
        
        # Insert content with color tags
        # Note: We'll use a simpler approach since Text widget doesn't support HTML span tags
        self.terminal_text.insert(tk.END, "╔═══════════════════════════════════════════════════════════════╗\n")
        self.terminal_text.insert(tk.END, "║                     Welcome to Theme Viz                      ║\n", 'normal')
        self.terminal_text.insert(tk.END, "╠═══════════════════════════════════════════════════════════════╣\n", 'normal')
        self.terminal_text.insert(tk.END, "║                                                               ║\n", 'normal')
        
        # Insert the prompt
        self.terminal_text.insert(tk.END, "║ ", 'normal')
        self.terminal_text.insert(tk.END, "user@theme-viz", 'red')
        self.terminal_text.insert(tk.END, ":~$ ", 'normal')
        self.terminal_text.insert(tk.END, "ls -la\n", 'green')
        
        # Continue with more sample content
        self.terminal_text.insert(tk.END, "║                                                               ║\n", 'normal')
        self.terminal_text.insert(tk.END, "║ total 48                                                      ║\n", 'normal')
        self.terminal_text.insert(tk.END, "║ drwxr-xr-x 12 user user 4096 Nov 26 09:26 .                   ║\n", 'bright_black')
        self.terminal_text.insert(tk.END, "║ drwxr-xr-x  4 user user 4096 Nov 20 15:27 ..                  ║\n", 'bright_black')
        self.terminal_text.insert(tk.END, "║ -rw-r--r--  1 user user  220 Nov 20 15:27 .bash_logout        ║\n", 'bright_black')
        self.terminal_text.insert(tk.END, "║ -rw-r--r--  1 user user 3771 Nov 20 15:27 .bashrc            ║\n", 'bright_black')
        self.terminal_text.insert(tk.END, "║ -rw-r--r--  1 user user  807 Nov 20 15:27 .profile           ║\n", 'bright_black')
        self.terminal_text.insert(tk.END, "║ -rwxr-xr-x  1 user user  352 Nov 26 09:25 theme_generator.py                            ║\n", 'yellow')
        self.terminal_text.insert(tk.END, "║ -rw-r--r--  1 user user 1244 Nov 26 09:26 README.md                                     ║\n", 'cyan')
        self.terminal_text.insert(tk.END, "║                                                               ║\n", 'normal')
        
        # Add more commands to demonstrate different colors
        self.terminal_text.insert(tk.END, "║ ", 'normal')
        self.terminal_text.insert(tk.END, "user@theme-viz", 'red')
        self.terminal_text.insert(tk.END, ":~$ ", 'normal')
        self.terminal_text.insert(tk.END, "echo $SHELL\n", 'green')
        
        self.terminal_text.insert(tk.END, "║ ", 'normal')
        self.terminal_text.insert(tk.END, "/bin/bash\n", 'cyan')
        
        self.terminal_text.insert(tk.END, "║ ", 'normal')
        self.terminal_text.insert(tk.END, "user@theme-viz", 'red')
        self.terminal_text.insert(tk.END, ":~$ ", 'normal')
        self.terminal_text.insert(tk.END, "ls --color=always\n", 'green')
        
        self.terminal_text.insert(tk.END, "║                                                               ║\n", 'normal')
        self.terminal_text.insert(tk.END, "║ total 48                                                      ║\n", 'normal')
        self.terminal_text.insert(tk.END, "║ drwxr-xr-x 12 user user 4096 Nov 26 09:26 .                   ║\n", 'blue')
        self.terminal_text.insert(tk.END, "║ drwxr-xr-x  4 user user 4096 Nov 20 15:27 ..                  ║\n", 'blue')
        self.terminal_text.insert(tk.END, "║ -rw-r--r--  1 user user  220 Nov 20 15:27 .bash_logout        ║\n", 'blue')
        self.terminal_text.insert(tk.END, "║ -rw-r--r--  1 user user 3771 Nov 20 15:27 .bashrc            ║\n", 'blue')
        self.terminal_text.insert(tk.END, "║ -rw-r--r--  1 user user  807 Nov 20 15:27 .profile           ║\n", 'blue')
        self.terminal_text.insert(tk.END, "║ -rwxr-xr-x  1 user user  352 Nov 26 09:25 theme_generator.py                            ║\n", 'yellow')
        self.terminal_text.insert(tk.END, "║ -rw-r--r--  1 user user 1244 Nov 26 09:26 README.md                                     ║\n", 'cyan')
        self.terminal_text.insert(tk.END, "║                                                               ║\n", 'normal')
        
        # Add final prompt
        self.terminal_text.insert(tk.END, "║ ", 'normal')
        self.terminal_text.insert(tk.END, "user@theme-viz", 'red')
        self.terminal_text.insert(tk.END, ":~$ ", 'normal')
        self.terminal_text.insert(tk.END, "_\b", 'cursor')  # Create a blinking cursor effect
        
        # Configure tag colors
        for tag, color in [
            ('normal', self.colors['foreground']),
            ('black', self.colors['black']),
            ('red', self.colors['red']),
            ('green', self.colors['green']),
            ('yellow', self.colors['yellow']),
            ('blue', self.colors['blue']),
            ('magenta', self.colors['magenta']),
            ('cyan', self.colors['cyan']),
            ('white', self.colors['white']),
            ('bright_black', self.colors['bright_black']),
            ('bright_red', self.colors['bright_red']),
            ('bright_green', self.colors['bright_green']),
            ('bright_yellow', self.colors['bright_yellow']),
            ('bright_blue', self.colors['bright_blue']),
            ('bright_magenta', self.colors['bright_magenta']),
            ('bright_cyan', self.colors['bright_cyan']),
            ('bright_white', self.colors['bright_white']),
            ('cursor', self.colors['cursor'])
        ]:
            self.terminal_text.tag_config(tag, foreground=color)
            
        # Make the text read-only
        self.terminal_text.config(state=tk.DISABLED)
        
    def update_colors(self, new_colors):
        """Update the preview with new colors."""
        self.colors = new_colors.copy()
        self.setup_ui()
