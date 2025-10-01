"""
Text element for titles and labels
"""
from PyQt6.QtGui import QPainter, QFont, QColor, QPen
from PyQt6.QtCore import Qt, QRectF

from elements.base_element import DraggableElement
from models.project_state import ElementState, TextSettings


class TextElement(DraggableElement):
    """
    Text element for displaying titles, artist names, etc.
    """
    
    def __init__(self, state: ElementState, settings: TextSettings):
        super().__init__(state)
        self.settings = settings
        
    def paint(self, painter: QPainter, option, widget):
        """Render the text"""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        
        # Setup font
        font = QFont(self.settings.font_family, self.settings.font_size)
        font.setBold(self.settings.bold)
        painter.setFont(font)
        
        # Setup color
        color = QColor(*self.settings.color)
        painter.setPen(color)
        
        # Draw text
        rect = QRectF(0, 0, self.state.width, self.state.height)
        painter.drawText(rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, 
                        self.settings.content)
        
        # Draw selection border and handles if selected
        super().paint(painter, option, widget)
    
    def update_size_from_text(self):
        """Auto-adjust element size based on text content"""
        # Create a temporary painter to measure text
        from PyQt6.QtGui import QFontMetrics
        
        font = QFont(self.settings.font_family, self.settings.font_size)
        font.setBold(self.settings.bold)
        metrics = QFontMetrics(font)
        
        # Calculate required size
        text_rect = metrics.boundingRect(self.settings.content)
        
        self.prepareGeometryChange()
        self.state.width = max(100, text_rect.width() + 20)
        self.state.height = max(50, text_rect.height() + 10)
        self.update()
