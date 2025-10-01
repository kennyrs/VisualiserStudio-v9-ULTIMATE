"""
Lyrics element with LRC synchronization
"""
from PyQt6.QtGui import QPainter, QFont, QColor, QPen, QFontMetrics
from PyQt6.QtCore import Qt, QRectF

from elements.base_element import DraggableElement
from models.project_state import ElementState
from models.lyrics_parser import LyricsParser


class LyricsElement(DraggableElement):
    """
    Synchronized lyrics display element
    """
    
    def __init__(self, state: ElementState, lyrics_parser: LyricsParser):
        super().__init__(state)
        self.lyrics_parser = lyrics_parser
        
        # Display settings
        self.font_family = "Arial"
        self.font_size = 48
        self.bold = True
        self.current_color = (255, 255, 255)
        self.inactive_color = (150, 150, 150)
        self.highlight_color = (255, 200, 0)
        
        # Display mode
        self.mode = "single"  # single, karaoke, window
        self.window_lines_before = 1
        self.window_lines_after = 2
        
        # Animation
        self.fade_in_time = 0.3
        self.fade_out_time = 0.3
        
        self.current_time = 0.0
    
    def paint(self, painter: QPainter, option, widget):
        """Render the lyrics"""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        
        if self.mode == "single":
            self._draw_single_line(painter)
        elif self.mode == "karaoke":
            self._draw_karaoke(painter)
        elif self.mode == "window":
            self._draw_window(painter)
        
        # Draw selection border and handles if selected
        super().paint(painter, option, widget)
    
    def _draw_single_line(self, painter: QPainter):
        """Draw single current lyric line"""
        lyric = self.lyrics_parser.get_current_lyric(self.current_time)
        
        if not lyric:
            return
        
        # Setup font
        font = QFont(self.font_family, self.font_size)
        font.setBold(self.bold)
        painter.setFont(font)
        
        # Setup color
        color = QColor(*self.current_color)
        painter.setPen(color)
        
        # Draw text centered
        rect = QRectF(0, 0, self.state.width, self.state.height)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, lyric)
    
    def _draw_karaoke(self, painter: QPainter):
        """Draw karaoke-style highlighting"""
        # Get current lyric and timing
        lyric = self.lyrics_parser.get_current_lyric(self.current_time)
        
        if not lyric:
            return
        
        # Setup font
        font = QFont(self.font_family, self.font_size)
        font.setBold(self.bold)
        painter.setFont(font)
        
        # Calculate progress within current line
        # This is simplified - real karaoke would need word-level timing
        progress = 0.5  # For now, just show current line highlighted
        
        # Draw text with highlight
        color = QColor(*self.highlight_color)
        painter.setPen(color)
        
        rect = QRectF(0, 0, self.state.width, self.state.height)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, lyric)
    
    def _draw_window(self, painter: QPainter):
        """Draw multiple lines (past, current, future)"""
        lines = self.lyrics_parser.get_lyric_window(
            self.current_time,
            self.window_lines_before,
            self.window_lines_after
        )
        
        if not lines:
            return
        
        # Setup font
        font = QFont(self.font_family, self.font_size)
        font.setBold(self.bold)
        painter.setFont(font)
        
        # Calculate line spacing
        metrics = QFontMetrics(font)
        line_height = metrics.height() + 10
        
        # Calculate starting Y position to center the window
        total_height = len(lines) * line_height
        start_y = (self.state.height - total_height) / 2
        
        # Draw each line
        for i, (text, is_current) in enumerate(lines):
            y = start_y + i * line_height
            
            # Color based on state
            if is_current:
                color = QColor(*self.current_color)
            else:
                color = QColor(*self.inactive_color)
            
            painter.setPen(color)
            
            # Draw text
            rect = QRectF(0, y, self.state.width, line_height)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
    
    def update_time(self, time_pos: float):
        """Update current time position"""
        self.current_time = time_pos
        self.update()
    
    def set_display_mode(self, mode: str):
        """Set display mode: single, karaoke, window"""
        if mode in ["single", "karaoke", "window"]:
            self.mode = mode
            self.update()
    
    def set_colors(self, current: tuple, inactive: tuple = None, highlight: tuple = None):
        """Set custom colors"""
        self.current_color = current
        if inactive:
            self.inactive_color = inactive
        if highlight:
            self.highlight_color = highlight
        self.update()
