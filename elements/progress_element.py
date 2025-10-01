"""
Progress bar element showing playback position
"""
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import Qt, QRectF

from elements.base_element import DraggableElement
from models.project_state import ElementState


class ProgressBarElement(DraggableElement):
    """
    Progress bar showing current playback position
    """
    
    def __init__(self, state: ElementState, style: str = "solid"):
        super().__init__(state)
        self.style = style
        self.progress = 0.0  # 0.0 to 1.0
        
        # Style colors
        self.filled_color = QColor(0, 180, 255)
        self.empty_color = QColor(60, 60, 60)
        self.border_color = QColor(100, 100, 100)
    
    def paint(self, painter: QPainter, option, widget):
        """Render the progress bar"""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.state.width
        height = self.state.height
        
        if self.style == "solid":
            self._draw_solid(painter, width, height)
        elif self.style == "pill":
            self._draw_pill(painter, width, height)
        elif self.style == "segmented":
            self._draw_segmented(painter, width, height)
        elif self.style == "dashed":
            self._draw_dashed(painter, width, height)
        else:
            self._draw_solid(painter, width, height)
        
        # Draw selection border and handles if selected
        super().paint(painter, option, widget)
    
    def _draw_solid(self, painter: QPainter, width: float, height: float):
        """Draw solid progress bar"""
        # Background
        painter.setBrush(QBrush(self.empty_color))
        painter.setPen(QPen(self.border_color, 1))
        painter.drawRect(QRectF(0, 0, width, height))
        
        # Progress fill
        fill_width = width * self.progress
        painter.setBrush(QBrush(self.filled_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(QRectF(0, 0, fill_width, height))
    
    def _draw_pill(self, painter: QPainter, width: float, height: float):
        """Draw rounded pill progress bar"""
        radius = min(height / 2, 10)
        
        # Background
        painter.setBrush(QBrush(self.empty_color))
        painter.setPen(QPen(self.border_color, 1))
        painter.drawRoundedRect(QRectF(0, 0, width, height), radius, radius)
        
        # Progress fill
        fill_width = width * self.progress
        if fill_width > 0:
            painter.setBrush(QBrush(self.filled_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(0, 0, fill_width, height), radius, radius)
    
    def _draw_segmented(self, painter: QPainter, width: float, height: float):
        """Draw segmented progress bar"""
        segments = 20
        gap = 2
        segment_width = (width - (segments - 1) * gap) / segments
        
        for i in range(segments):
            x = i * (segment_width + gap)
            
            # Determine if segment should be filled
            segment_progress = (i + 1) / segments
            if segment_progress <= self.progress:
                color = self.filled_color
            else:
                color = self.empty_color
            
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(QRectF(x, 0, segment_width, height))
    
    def _draw_dashed(self, painter: QPainter, width: float, height: float):
        """Draw dashed progress bar"""
        dash_length = 20
        gap_length = 10
        
        painter.setPen(Qt.PenStyle.NoPen)
        
        x = 0
        while x < width:
            # Determine color
            if x / width <= self.progress:
                color = self.filled_color
            else:
                color = self.empty_color
            
            painter.setBrush(QBrush(color))
            
            # Draw dash
            dash_width = min(dash_length, width - x)
            painter.drawRect(QRectF(x, height * 0.3, dash_width, height * 0.4))
            
            x += dash_length + gap_length
    
    def update_progress(self, current_time: float, total_time: float):
        """Update progress based on time"""
        if total_time > 0:
            self.progress = min(1.0, max(0.0, current_time / total_time))
        else:
            self.progress = 0.0
        self.update()
    
    def set_colors(self, filled: QColor, empty: QColor, border: QColor = None):
        """Set custom colors"""
        self.filled_color = filled
        self.empty_color = empty
        if border:
            self.border_color = border
        self.update()
