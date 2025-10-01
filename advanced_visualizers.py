"""
Additional advanced visualizers: DOTS, WAVEFORM, PIXEL_EQ, RIBBON, AREA
"""
import numpy as np
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QPointF
import math


class DotsVisualizer:
    """Particle/dots visualizer that jumps with audio"""
    
    @staticmethod
    def draw(painter: QPainter, spectrum: np.ndarray, width: float, height: float,
             gradient_func, num_particles: int = 50):
        """
        Draw dots visualizer
        
        Args:
            painter: QPainter instance
            spectrum: Audio spectrum array
            width, height: Drawing area dimensions
            gradient_func: Function to get gradient color
            num_particles: Number of particles
        """
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        
        # Calculate particle positions
        particles_per_band = max(1, num_particles // len(spectrum))
        
        for i, level in enumerate(spectrum):
            # Get color from gradient
            color = gradient_func(i / len(spectrum))
            painter.setBrush(QBrush(color))
            
            # Position along width
            band_width = width / len(spectrum)
            x_center = i * band_width + band_width / 2
            
            # Particle size based on level
            base_size = 3
            size = base_size + level * 8
            
            # Y position with bounce
            y_base = height / 2
            y_offset = level * (height / 2 - 20)
            
            # Draw main particle
            painter.drawEllipse(
                QPointF(x_center, y_base - y_offset),
                size, size
            )
            
            # Draw secondary particles for high levels
            if level > 0.7:
                # Top particle
                painter.drawEllipse(
                    QPointF(x_center, y_base - y_offset - 20),
                    size * 0.6, size * 0.6
                )
                # Bottom particle
                painter.drawEllipse(
                    QPointF(x_center, y_base + y_offset + 20),
                    size * 0.6, size * 0.6
                )


class WaveformVisualizer:
    """Classic audio waveform display"""
    
    @staticmethod
    def draw(painter: QPainter, spectrum: np.ndarray, width: float, height: float,
             gradient_func, line_thickness: int = 2):
        """Draw waveform visualizer"""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center_y = height / 2
        
        # Upper waveform
        path_upper = QPainterPath()
        path_upper.moveTo(0, center_y)
        
        for i, level in enumerate(spectrum):
            x = (i / len(spectrum)) * width
            y = center_y - (level * height / 2)
            path_upper.lineTo(x, y)
        
        # Draw upper waveform
        color = gradient_func(0.3)
        pen = QPen(color, line_thickness)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path_upper)
        
        # Lower waveform (mirrored)
        path_lower = QPainterPath()
        path_lower.moveTo(0, center_y)
        
        for i, level in enumerate(spectrum):
            x = (i / len(spectrum)) * width
            y = center_y + (level * height / 2)
            path_lower.lineTo(x, y)
        
        # Draw lower waveform
        color = gradient_func(0.7)
        pen = QPen(color, line_thickness)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawPath(path_lower)


class PixelEQVisualizer:
    """Retro pixel/8-bit style equalizer"""
    
    @staticmethod
    def draw(painter: QPainter, spectrum: np.ndarray, width: float, height: float,
             gradient_func, pixel_size: int = 8):
        """Draw pixel EQ visualizer"""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)  # Crisp pixels
        painter.setPen(Qt.PenStyle.NoPen)
        
        num_bands = len(spectrum)
        band_width = width / num_bands
        
        # Ensure band_width is multiple of pixel_size
        band_width = (band_width // pixel_size) * pixel_size
        
        for i, level in enumerate(spectrum):
            x = i * band_width
            
            # Calculate number of pixel rows
            max_rows = int(height / pixel_size)
            active_rows = int(level * max_rows)
            
            # Get color
            color = gradient_func(i / num_bands)
            painter.setBrush(QBrush(color))
            
            # Draw pixels from bottom up
            for row in range(active_rows):
                y = height - (row + 1) * pixel_size
                
                # Vary color intensity by row
                intensity = 0.5 + 0.5 * (row / max(1, active_rows))
                row_color = QColor(
                    int(color.red() * intensity),
                    int(color.green() * intensity),
                    int(color.blue() * intensity)
                )
                painter.setBrush(QBrush(row_color))
                
                painter.drawRect(QRectF(x, y, band_width - pixel_size, pixel_size - 1))


class RibbonVisualizer:
    """Flowing ribbon/wave visualizer"""
    
    @staticmethod
    def draw(painter: QPainter, spectrum: np.ndarray, width: float, height: float,
             gradient_func, ribbon_width: float = 40):
        """Draw ribbon visualizer"""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center_y = height / 2
        
        # Create ribbon path
        path = QPainterPath()
        
        # Start point
        path.moveTo(0, center_y)
        
        # Upper curve
        for i, level in enumerate(spectrum):
            x = (i / len(spectrum)) * width
            y = center_y - (level * height / 3)
            
            if i == 0:
                path.lineTo(x, y)
            else:
                # Use quadratic curve for smoothness
                prev_i = i - 1
                prev_x = (prev_i / len(spectrum)) * width
                prev_level = spectrum[prev_i]
                prev_y = center_y - (prev_level * height / 3)
                
                control_x = (prev_x + x) / 2
                control_y = (prev_y + y) / 2
                
                path.quadTo(control_x, control_y, x, y)
        
        # Connect to lower curve
        for i in range(len(spectrum) - 1, -1, -1):
            x = (i / len(spectrum)) * width
            level = spectrum[i]
            y = center_y - (level * height / 3) + ribbon_width
            path.lineTo(x, y)
        
        # Close path
        path.closeSubpath()
        
        # Create gradient brush
        # For now, use solid color from gradient
        color = gradient_func(0.5)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.PenStyle.NoPen)
        
        painter.drawPath(path)
        
        # Draw outline
        outline_color = QColor(color)
        outline_color.setAlpha(200)
        pen = QPen(outline_color, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)


class AreaVisualizer:
    """Filled area under line visualizer"""
    
    @staticmethod
    def draw(painter: QPainter, spectrum: np.ndarray, width: float, height: float,
             gradient_func):
        """Draw area visualizer"""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create path for area
        path = QPainterPath()
        path.moveTo(0, height)
        
        # Line through spectrum
        for i, level in enumerate(spectrum):
            x = (i / len(spectrum)) * width
            y = height - (level * height)
            
            if i == 0:
                path.lineTo(x, y)
            else:
                # Smooth curve
                prev_i = i - 1
                prev_x = (prev_i / len(spectrum)) * width
                prev_level = spectrum[prev_i]
                prev_y = height - (prev_level * height)
                
                control_x = (prev_x + x) / 2
                control_y = (prev_y + y) / 2
                
                path.quadTo(control_x, control_y, x, y)
        
        # Complete the area
        path.lineTo(width, height)
        path.closeSubpath()
        
        # Fill with gradient-like color
        # Create vertical gradient effect by filling in layers
        num_layers = 10
        for layer in range(num_layers):
            alpha = int(255 * (1 - layer / num_layers) * 0.8)
            color = gradient_func(layer / num_layers)
            color.setAlpha(alpha)
            
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPath(path)


class SpiralVisualizer:
    """Spiral/helix visualizer"""
    
    @staticmethod
    def draw(painter: QPainter, spectrum: np.ndarray, width: float, height: float,
             gradient_func, num_spirals: int = 3):
        """Draw spiral visualizer"""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center_x = width / 2
        center_y = height / 2
        max_radius = min(width, height) / 2 - 20
        
        for spiral_idx in range(num_spirals):
            path = QPainterPath()
            
            angle_offset = (spiral_idx / num_spirals) * 360
            
            for i, level in enumerate(spectrum):
                angle = (i / len(spectrum)) * 720 + angle_offset  # 2 full rotations
                angle_rad = math.radians(angle)
                
                # Radius increases with angle
                base_radius = (i / len(spectrum)) * max_radius
                radius = base_radius + level * 30
                
                x = center_x + radius * math.cos(angle_rad)
                y = center_y + radius * math.sin(angle_rad)
                
                if i == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)
            
            # Draw spiral
            color = gradient_func(spiral_idx / num_spirals)
            pen = QPen(color, 3)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(path)


class PulseCircleVisualizer:
    """Pulsing circles visualizer"""
    
    @staticmethod
    def draw(painter: QPainter, spectrum: np.ndarray, width: float, height: float,
             gradient_func):
        """Draw pulse circles"""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        
        center_x = width / 2
        center_y = height / 2
        
        # Calculate average level for pulsing
        avg_level = np.mean(spectrum)
        
        # Draw multiple circles
        num_circles = 5
        for i in range(num_circles):
            # Radius based on circle index and audio level
            base_radius = (i + 1) * 40
            radius = base_radius + avg_level * 50
            
            # Color and opacity
            color = gradient_func(i / num_circles)
            alpha = int(255 * (1 - i / num_circles) * 0.6)
            color.setAlpha(alpha)
            
            painter.setBrush(QBrush(color))
            painter.drawEllipse(
                QPointF(center_x, center_y),
                radius, radius
            )
