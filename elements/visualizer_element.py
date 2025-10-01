"""
Visualizer element with real-time FFT rendering
ALL 12 VISUALIZER TYPES INCLUDED
"""
import numpy as np
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QPointF
import math

from elements.base_element import DraggableElement
from models.project_state import ElementState, VisualizerSettings
from models.audio_processor import AudioProcessor
from utils.config import GRADIENTS, VisualizerType
from core.advanced_visualizers import (DotsVisualizer, WaveformVisualizer, 
                                       PixelEQVisualizer, RibbonVisualizer, 
                                       AreaVisualizer, SpiralVisualizer, 
                                       PulseCircleVisualizer)


class VisualizerElement(DraggableElement):
    """
    Visualizer element that displays audio spectrum
    Supports 12 different visualizer types
    """
    
    def __init__(self, state: ElementState, settings: VisualizerSettings, 
                 audio_processor: AudioProcessor):
        super().__init__(state)
        self.settings = settings
        self.audio_processor = audio_processor
        
        # Current spectrum data
        self.current_spectrum = np.zeros(settings.eq_bands)
        self.prev_spectrum = np.zeros(settings.eq_bands)
        
    def paint(self, painter: QPainter, option, widget):
        """Render the visualizer"""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw visualizer based on type
        viz_type = self.settings.visualizer_type
        
        if viz_type == VisualizerType.BARS:
            self._draw_bars(painter)
        elif viz_type == VisualizerType.MIRROR_BARS:
            self._draw_mirror_bars(painter)
        elif viz_type == VisualizerType.LINE:
            self._draw_line(painter)
        elif viz_type == VisualizerType.CIRCULAR:
            self._draw_circular(painter)
        elif viz_type == VisualizerType.RING:
            self._draw_ring(painter)
        elif viz_type == VisualizerType.AREA:
            AreaVisualizer.draw(painter, self.current_spectrum, 
                               self.state.width, self.state.height, 
                               self._get_gradient_color)
        elif viz_type == VisualizerType.DOTS:
            DotsVisualizer.draw(painter, self.current_spectrum, 
                               self.state.width, self.state.height, 
                               self._get_gradient_color)
        elif viz_type == VisualizerType.WAVEFORM:
            WaveformVisualizer.draw(painter, self.current_spectrum, 
                                   self.state.width, self.state.height, 
                                   self._get_gradient_color, 
                                   self.settings.line_thickness)
        elif viz_type == VisualizerType.PIXEL_EQ:
            PixelEQVisualizer.draw(painter, self.current_spectrum, 
                                  self.state.width, self.state.height, 
                                  self._get_gradient_color)
        elif viz_type == VisualizerType.RIBBON:
            RibbonVisualizer.draw(painter, self.current_spectrum, 
                                 self.state.width, self.state.height, 
                                 self._get_gradient_color)
        elif viz_type == VisualizerType.SPIRAL:
            SpiralVisualizer.draw(painter, self.current_spectrum, 
                                 self.state.width, self.state.height, 
                                 self._get_gradient_color)
        elif viz_type == VisualizerType.PULSE_CIRCLE:
            PulseCircleVisualizer.draw(painter, self.current_spectrum, 
                                      self.state.width, self.state.height, 
                                      self._get_gradient_color)
        else:
            self._draw_bars(painter)  # Default
        
        # Draw selection border and handles if selected
        super().paint(painter, option, widget)
    
    def update_spectrum(self, time_pos: float):
        """Update spectrum data for current time position"""
        if self.audio_processor.audio is not None:
            spectrum = self.audio_processor.get_spectrum(
                time_pos, 
                self.settings.eq_bands
            )
            
            # Smooth interpolation
            self.current_spectrum = (
                self.prev_spectrum * (1 - self.settings.smoothness) +
                spectrum * self.settings.smoothness
            )
            self.prev_spectrum = self.current_spectrum.copy()
        else:
            # Generate random data for preview when no audio
            self.current_spectrum = np.random.random(self.settings.eq_bands) * 0.5
    
    def _get_gradient_color(self, position: float) -> QColor:
        """Get color from gradient at position (0-1)"""
        colors = GRADIENTS.get(self.settings.gradient, GRADIENTS["Ocean"])
        
        # Find segment
        num_colors = len(colors)
        segment = position * (num_colors - 1)
        idx = int(segment)
        t = segment - idx
        
        # Clamp index
        idx = max(0, min(idx, num_colors - 2))
        
        # Linear interpolation between two colors
        c1 = colors[idx]
        c2 = colors[idx + 1]
        
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        
        return QColor(r, g, b)
    
    def _draw_bars(self, painter: QPainter):
        """Draw classic bar equalizer"""
        width = self.state.width
        height = self.state.height
        num_bars = len(self.current_spectrum)
        
        bar_width = width / num_bars
        gap = 2
        
        for i, level in enumerate(self.current_spectrum):
            x = i * bar_width
            bar_height = level * height
            y = height - bar_height
            
            # Get gradient color
            color = self._get_gradient_color(i / num_bars)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            
            if self.settings.rounded_bars:
                # Rounded rectangle
                rect = QRectF(x + gap/2, y, bar_width - gap, bar_height)
                painter.drawRoundedRect(rect, 3, 3)
            else:
                # Regular rectangle
                rect = QRectF(x + gap/2, y, bar_width - gap, bar_height)
                painter.drawRect(rect)
    
    def _draw_mirror_bars(self, painter: QPainter):
        """Draw mirrored bars (top and bottom)"""
        width = self.state.width
        height = self.state.height
        num_bars = len(self.current_spectrum)
        
        bar_width = width / num_bars
        gap = 2
        mirror_gap = self.settings.mirror_gap
        
        half_height = (height - mirror_gap) / 2
        
        for i, level in enumerate(self.current_spectrum):
            x = i * bar_width
            bar_height = level * half_height
            
            # Get gradient color
            color = self._get_gradient_color(i / num_bars)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            
            # Top bars (growing down)
            y_top = half_height - bar_height
            rect_top = QRectF(x + gap/2, y_top, bar_width - gap, bar_height)
            
            # Bottom bars (growing up)
            y_bottom = half_height + mirror_gap
            rect_bottom = QRectF(x + gap/2, y_bottom, bar_width - gap, bar_height)
            
            if self.settings.rounded_bars:
                painter.drawRoundedRect(rect_top, 3, 3)
                painter.drawRoundedRect(rect_bottom, 3, 3)
            else:
                painter.drawRect(rect_top)
                painter.drawRect(rect_bottom)
    
    def _draw_line(self, painter: QPainter):
        """Draw smooth line visualizer"""
        width = self.state.width
        height = self.state.height
        num_points = len(self.current_spectrum)
        
        path = QPainterPath()
        
        # Start point
        x = 0
        y = height - self.current_spectrum[0] * height
        path.moveTo(x, y)
        
        # Draw smooth curve through points
        for i in range(1, num_points):
            x = (i / num_points) * width
            y = height - self.current_spectrum[i] * height
            path.lineTo(x, y)
        
        # Draw the line
        color = self._get_gradient_color(0.5)
        pen = QPen(color, self.settings.line_thickness)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)
    
    def _draw_circular(self, painter: QPainter):
        """Draw circular/radial visualizer"""
        width = self.state.width
        height = self.state.height
        center_x = width / 2
        center_y = height / 2
        
        # Radius for inner and outer circle
        max_radius = min(width, height) / 2 - 10
        min_radius = max_radius * 0.3
        
        num_bars = len(self.current_spectrum)
        angle_step = 360 / num_bars
        
        for i, level in enumerate(self.current_spectrum):
            angle = i * angle_step
            angle_rad = math.radians(angle - 90)  # Start from top
            
            # Calculate bar length
            bar_length = level * (max_radius - min_radius)
            
            # Start and end points
            x1 = center_x + min_radius * math.cos(angle_rad)
            y1 = center_y + min_radius * math.sin(angle_rad)
            x2 = center_x + (min_radius + bar_length) * math.cos(angle_rad)
            y2 = center_y + (min_radius + bar_length) * math.sin(angle_rad)
            
            # Get gradient color
            color = self._get_gradient_color(i / num_bars)
            pen = QPen(color, 3)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            
            painter.setPen(pen)
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
    
    def _draw_ring(self, painter: QPainter):
        """Draw ring visualizer"""
        width = self.state.width
        height = self.state.height
        center_x = width / 2
        center_y = height / 2
        
        base_radius = min(width, height) / 3
        num_bars = len(self.current_spectrum)
        angle_step = 360 / num_bars
        
        # Draw filled arcs
        for i, level in enumerate(self.current_spectrum):
            start_angle = int(i * angle_step * 16)  # Qt uses 1/16th degrees
            span_angle = int(angle_step * 16)
            
            # Ring thickness based on level
            thickness = level * (base_radius * 0.5)
            inner_radius = base_radius - thickness / 2
            outer_radius = base_radius + thickness / 2
            
            # Get gradient color
            color = self._get_gradient_color(i / num_bars)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            
            # Draw arc (this is simplified, proper ring drawing is more complex)
            rect = QRectF(
                center_x - outer_radius,
                center_y - outer_radius,
                outer_radius * 2,
                outer_radius * 2
            )
            painter.drawPie(rect, start_angle, span_angle)
"""
Visualizer element with real-time FFT rendering
"""
import numpy as np
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath
from PyQt6.QtCore import Qt, QRectF, QPointF
import math

from elements.base_element import DraggableElement
from models.project_state import ElementState, VisualizerSettings
from models.audio_processor import AudioProcessor
from utils.config import GRADIENTS, VisualizerType


class VisualizerElement(DraggableElement):
    """
    Visualizer element that displays audio spectrum
    """
    
    def __init__(self, state: ElementState, settings: VisualizerSettings, 
                 audio_processor: AudioProcessor):
        super().__init__(state)
        self.settings = settings
        self.audio_processor = audio_processor
        
        # Current spectrum data
        self.current_spectrum = np.zeros(settings.eq_bands)
        self.prev_spectrum = np.zeros(settings.eq_bands)
        
    def paint(self, painter: QPainter, option, widget):
        """Render the visualizer"""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw visualizer based on type
        if self.settings.visualizer_type == VisualizerType.BARS:
            self._draw_bars(painter)
        elif self.settings.visualizer_type == VisualizerType.MIRROR_BARS:
            self._draw_mirror_bars(painter)
        elif self.settings.visualizer_type == VisualizerType.LINE:
            self._draw_line(painter)
        elif self.settings.visualizer_type == VisualizerType.CIRCULAR:
            self._draw_circular(painter)
        elif self.settings.visualizer_type == VisualizerType.RING:
            self._draw_ring(painter)
        else:
            self._draw_bars(painter)  # Default
        
        # Draw selection border and handles if selected
        super().paint(painter, option, widget)
    
    def update_spectrum(self, time_pos: float):
        """Update spectrum data for current time position"""
        if self.audio_processor.audio is not None:
            spectrum = self.audio_processor.get_spectrum(
                time_pos, 
                self.settings.eq_bands
            )
            
            # Smooth interpolation
            self.current_spectrum = (
                self.prev_spectrum * (1 - self.settings.smoothness) +
                spectrum * self.settings.smoothness
            )
            self.prev_spectrum = self.current_spectrum.copy()
        else:
            # Generate random data for preview when no audio
            self.current_spectrum = np.random.random(self.settings.eq_bands) * 0.5
    
    def _get_gradient_color(self, position: float) -> QColor:
        """Get color from gradient at position (0-1)"""
        colors = GRADIENTS.get(self.settings.gradient, GRADIENTS["Ocean"])
        
        # Find segment
        num_colors = len(colors)
        segment = position * (num_colors - 1)
        idx = int(segment)
        t = segment - idx
        
        # Clamp index
        idx = max(0, min(idx, num_colors - 2))
        
        # Linear interpolation between two colors
        c1 = colors[idx]
        c2 = colors[idx + 1]
        
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        
        return QColor(r, g, b)
    
    def _draw_bars(self, painter: QPainter):
        """Draw classic bar equalizer"""
        width = self.state.width
        height = self.state.height
        num_bars = len(self.current_spectrum)
        
        bar_width = width / num_bars
        gap = 2
        
        for i, level in enumerate(self.current_spectrum):
            x = i * bar_width
            bar_height = level * height
            y = height - bar_height
            
            # Get gradient color
            color = self._get_gradient_color(i / num_bars)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            
            if self.settings.rounded_bars:
                # Rounded rectangle
                rect = QRectF(x + gap/2, y, bar_width - gap, bar_height)
                painter.drawRoundedRect(rect, 3, 3)
            else:
                # Regular rectangle
                rect = QRectF(x + gap/2, y, bar_width - gap, bar_height)
                painter.drawRect(rect)
    
    def _draw_mirror_bars(self, painter: QPainter):
        """Draw mirrored bars (top and bottom)"""
        width = self.state.width
        height = self.state.height
        num_bars = len(self.current_spectrum)
        
        bar_width = width / num_bars
        gap = 2
        mirror_gap = self.settings.mirror_gap
        
        half_height = (height - mirror_gap) / 2
        
        for i, level in enumerate(self.current_spectrum):
            x = i * bar_width
            bar_height = level * half_height
            
            # Get gradient color
            color = self._get_gradient_color(i / num_bars)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            
            # Top bars (growing down)
            y_top = half_height - bar_height
            rect_top = QRectF(x + gap/2, y_top, bar_width - gap, bar_height)
            
            # Bottom bars (growing up)
            y_bottom = half_height + mirror_gap
            rect_bottom = QRectF(x + gap/2, y_bottom, bar_width - gap, bar_height)
            
            if self.settings.rounded_bars:
                painter.drawRoundedRect(rect_top, 3, 3)
                painter.drawRoundedRect(rect_bottom, 3, 3)
            else:
                painter.drawRect(rect_top)
                painter.drawRect(rect_bottom)
    
    def _draw_line(self, painter: QPainter):
        """Draw smooth line visualizer"""
        width = self.state.width
        height = self.state.height
        num_points = len(self.current_spectrum)
        
        path = QPainterPath()
        
        # Start point
        x = 0
        y = height - self.current_spectrum[0] * height
        path.moveTo(x, y)
        
        # Draw smooth curve through points
        for i in range(1, num_points):
            x = (i / num_points) * width
            y = height - self.current_spectrum[i] * height
            path.lineTo(x, y)
        
        # Draw the line
        color = self._get_gradient_color(0.5)
        pen = QPen(color, self.settings.line_thickness)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)
    
    def _draw_circular(self, painter: QPainter):
        """Draw circular/radial visualizer"""
        width = self.state.width
        height = self.state.height
        center_x = width / 2
        center_y = height / 2
        
        # Radius for inner and outer circle
        max_radius = min(width, height) / 2 - 10
        min_radius = max_radius * 0.3
        
        num_bars = len(self.current_spectrum)
        angle_step = 360 / num_bars
        
        for i, level in enumerate(self.current_spectrum):
            angle = i * angle_step
            angle_rad = math.radians(angle - 90)  # Start from top
            
            # Calculate bar length
            bar_length = level * (max_radius - min_radius)
            
            # Start and end points
            x1 = center_x + min_radius * math.cos(angle_rad)
            y1 = center_y + min_radius * math.sin(angle_rad)
            x2 = center_x + (min_radius + bar_length) * math.cos(angle_rad)
            y2 = center_y + (min_radius + bar_length) * math.sin(angle_rad)
            
            # Get gradient color
            color = self._get_gradient_color(i / num_bars)
            pen = QPen(color, 3)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            
            painter.setPen(pen)
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
    
    def _draw_ring(self, painter: QPainter):
        """Draw ring visualizer"""
        width = self.state.width
        height = self.state.height
        center_x = width / 2
        center_y = height / 2
        
        base_radius = min(width, height) / 3
        num_bars = len(self.current_spectrum)
        angle_step = 360 / num_bars
        
        # Draw filled arcs
        for i, level in enumerate(self.current_spectrum):
            start_angle = int(i * angle_step * 16)  # Qt uses 1/16th degrees
            span_angle = int(angle_step * 16)
            
            # Ring thickness based on level
            thickness = level * (base_radius * 0.5)
            inner_radius = base_radius - thickness / 2
            outer_radius = base_radius + thickness / 2
            
            # Get gradient color
            color = self._get_gradient_color(i / num_bars)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            
            # Draw arc (this is simplified, proper ring drawing is more complex)
            rect = QRectF(
                center_x - outer_radius,
                center_y - outer_radius,
                outer_radius * 2,
                outer_radius * 2
            )
            painter.drawPie(rect, start_angle, span_angle)
