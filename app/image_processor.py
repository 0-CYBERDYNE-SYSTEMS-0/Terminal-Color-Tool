"""
Image Color Processor for the Theme Creator

This module provides functionality to extract colors from images
for use in terminal theme creation.
"""

import os
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import colorsys


class ImageProcessor:
    """Processes images to extract color palettes."""
    
    def __init__(self):
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp']
        
    def is_supported_image(self, file_path):
        """Check if the file is a supported image format."""
        if not os.path.isfile(file_path):
            return False
            
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.supported_formats
        
    def extract_colors(self, image_path, num_colors=16, extract_method='kmeans'):
        """
        Extract colors from an image.
        
        Args:
            image_path (str): Path to the image file
            num_colors (int): Number of colors to extract
            extract_method (str): Method to use ('kmeans', 'median_cut', 'simple')
            
        Returns:
            dict: Dictionary mapping color names to hex values
        """
        if not self.is_supported_image(image_path):
            return None
            
        try:
            # Open and resize image for faster processing
            with Image.open(image_path) as img:
                img = img.convert('RGB')
                img = img.resize((150, 150))  # Resize for faster processing
                
                # Convert image to numpy array
                img_array = np.array(img)
                pixels = img_array.reshape(-1, 3)
                
                # Extract colors based on method
                if extract_method == 'kmeans':
                    colors = self._extract_kmeans(pixels, num_colors)
                elif extract_method == 'median_cut':
                    colors = self._extract_median_cut(pixels, num_colors)
                else:  # simple method
                    colors = self._extract_simple(pixels, num_colors)
                
                # Sort colors by frequency
                color_counts = {}
                for pixel in pixels:
                    color = self._rgb_to_hex(pixel[0], pixel[1], pixel[2])
                    color_counts[color] = color_counts.get(color, 0) + 1
                
                # Sort extracted colors by frequency
                sorted_colors = sorted(colors, 
                                    key=lambda c: color_counts.get(c, 0), 
                                    reverse=True)
                
                # Map to terminal color names
                terminal_colors = self._map_to_terminal_colors(sorted_colors[:num_colors])
                
                return terminal_colors
                
        except Exception as e:
            print(f"Error processing image: {e}")
            return None
            
    def _extract_kmeans(self, pixels, num_colors):
        """Extract colors using K-means clustering."""
        # Use K-means to find dominant colors
        kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        # Get cluster centers (colors)
        colors = kmeans.cluster_centers_.astype(int)
        
        # Convert to hex
        hex_colors = []
        for color in colors:
            hex_colors.append(self._rgb_to_hex(color[0], color[1], color[2]))
            
        return hex_colors
        
    def _extract_median_cut(self, pixels, num_colors):
        """Extract colors using median cut algorithm."""
        # For simplicity, we'll use a variation of this
        # Group similar colors first
        unique_pixels = np.unique(pixels, axis=0)
        
        if len(unique_pixels) <= num_colors:
            return [self._rgb_to_hex(p[0], p[1], p[2]) for p in unique_pixels]
        
        # Simple approach: sort by brightness and pick evenly spaced colors
        brightness_values = [self._calculate_brightness(p[0], p[1], p[2]) for p in unique_pixels]
        sorted_indices = np.argsort(brightness_values)
        
        step = len(sorted_indices) // num_colors
        selected_indices = sorted_indices[::step][:num_colors]
        
        hex_colors = []
        for idx in selected_indices:
            color = unique_pixels[idx]
            hex_colors.append(self._rgb_to_hex(color[0], color[1], color[2]))
            
        return hex_colors
        
    def _extract_simple(self, pixels, num_colors):
        """Simple color extraction by sampling."""
        # Randomly sample pixels and find most common
        np.random.seed(42)
        sample_indices = np.random.choice(len(pixels), min(1000, len(pixels)), replace=False)
        sample_pixels = pixels[sample_indices]
        
        # Get unique colors from sample
        unique_colors = np.unique(sample_pixels, axis=0)
        
        # Convert to hex
        hex_colors = []
        for color in unique_colors[:num_colors]:
            hex_colors.append(self._rgb_to_hex(color[0], color[1], color[2]))
            
        return hex_colors
        
    def _map_to_terminal_colors(self, extracted_colors):
        """
        Map extracted colors to terminal color names.
        
        Args:
            extracted_colors (list): List of hex color strings
            
        Returns:
            dict: Terminal colors mapped to extracted colors
        """
        if len(extracted_colors) == 0:
            return {}
            
        terminal_colors = {}
        
        # Always use the darkest color for background
        if len(extracted_colors) > 0:
            background = min(extracted_colors, key=self._brightness)
            terminal_colors['background'] = background
            extracted_colors.remove(background)
            
        # Always use the brightest/lightest color for foreground
        if len(extracted_colors) > 0:
            foreground = max(extracted_colors, key=self._brightness)
            terminal_colors['foreground'] = foreground
            extracted_colors.remove(foreground)
            
        # Use the brightest remaining color for cursor
        if len(extracted_colors) > 0:
            cursor = max(extracted_colors, key=self._brightness)
            terminal_colors['cursor'] = cursor
            extracted_colors.remove(cursor)
            
        # Map remaining colors to terminal color names
        color_mappings = [
            ('black', 'darkest'),
            ('white', 'brightest'),
            ('red', 'most_red'),
            ('green', 'most_green'),
            ('yellow', 'most_yellow'),
            ('blue', 'most_blue'),
            ('magenta', 'most_magenta'),
            ('cyan', 'most_cyan'),
            ('bright_black', 'second_darkest'),
            ('bright_red', 'brightest_red'),
            ('bright_green', 'brightest_green'),
            ('bright_yellow', 'brightest_yellow'),
            ('bright_blue', 'brightest_blue'),
            ('bright_magenta', 'brightest_magenta'),
            ('bright_cyan', 'brightest_cyan'),
            ('bright_white', 'second_brightest')
        ]
        
        for color_name, criteria in color_mappings:
            if len(extracted_colors) > 0:
                if criteria == 'darkest':
                    selected = min(extracted_colors, key=self._brightness)
                elif criteria == 'brightest':
                    selected = max(extracted_colors, key=self._brightness)
                elif criteria == 'second_darkest':
                    sorted_colors = sorted(extracted_colors, key=self._brightness)
                    selected = sorted_colors[1] if len(sorted_colors) > 1 else sorted_colors[0]
                elif criteria == 'second_brightest':
                    sorted_colors = sorted(extracted_colors, key=self._brightness, reverse=True)
                    selected = sorted_colors[1] if len(sorted_colors) > 1 else sorted_colors[0]
                elif criteria.startswith('most_'):
                    channel = criteria.split('_')[1]
                    selected = max(extracted_colors, key=lambda c: self._get_channel_value(c, channel))
                elif criteria.startswith('brightest_'):
                    channel = criteria.split('_')[1]
                    # Sort by brightness first, then by channel intensity
                    sorted_colors = sorted(extracted_colors, 
                                         key=lambda c: (self._brightness(c), self._get_channel_value(c, channel)),
                                         reverse=True)
                    selected = sorted_colors[0]
                else:
                    selected = extracted_colors[0]
                    
                terminal_colors[color_name] = selected
                extracted_colors.remove(selected)
                
        # Fill any missing colors with defaults
        defaults = {
            'black': '#000000',
            'red': '#FF0000',
            'green': '#00FF00',
            'yellow': '#FFFF00',
            'blue': '#0000FF',
            'magenta': '#FF00FF',
            'cyan': '#00FFFF',
            'white': '#FFFFFF'
        }
        
        for color_name in ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']:
            if color_name not in terminal_colors and color_name in defaults:
                terminal_colors[color_name] = defaults[color_name]
                
        # Generate bright variants by increasing lightness
        for base_color in ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']:
            if base_color in terminal_colors:
                bright_name = f'bright_{base_color}'
                terminal_colors[bright_name] = self._make_brighter(terminal_colors[base_color])
                
        return terminal_colors
        
    def _rgb_to_hex(self, r, g, b):
        """Convert RGB values to hex string."""
        return f"#{r:02x}{g:02x}{b:02x}"
        
    def _hex_to_rgb(self, hex_color):
        """Convert hex string to RGB values."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
    def _brightness(self, hex_color):
        """Calculate brightness of a hex color."""
        r, g, b = self._hex_to_rgb(hex_color)
        return self._calculate_brightness(r, g, b)
        
    def _calculate_brightness(self, r, g, b):
        """Calculate brightness using relative luminance formula."""
        return 0.299 * r + 0.587 * g + 0.114 * b
        
    def _get_channel_value(self, hex_color, channel):
        """Get the value of a specific color channel."""
        r, g, b = self._hex_to_rgb(hex_color)
        if channel == 'red':
            return r
        elif channel == 'green':
            return g
        elif channel == 'blue':
            return b
        return 0
        
    def _make_brighter(self, hex_color):
        """Make a color brighter by increasing its lightness."""
        r, g, b = self._hex_to_rgb(hex_color)
        
        # Convert to HSV
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        
        # Increase lightness (value) and slightly reduce saturation
        s = max(0, s - 0.1)  # Reduce saturation slightly
        v = min(1.0, v + 0.2)  # Increase brightness
        
        # Convert back to RGB
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        
        # Convert to hex
        return self._rgb_to_hex(int(r * 255), int(g * 255), int(b * 255))
