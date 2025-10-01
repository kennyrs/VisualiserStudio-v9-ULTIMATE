"""
Preview widget with play/pause controls and canvas
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                              QSlider, QLabel, QGraphicsView, QGraphicsScene)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QRectF
from PyQt6.QtGui import QPainter, QPixmap, QBrush, QColor
from typing import Optional, List

from models.audio_processor import AudioProcessor
from models.project_state import ProjectState
from elements.base_element import DraggableElement
from utils.config import PREVIEW_FPS, DEFAULT_WIDTH, DEFAULT_HEIGHT


class PreviewScene(QGraphicsScene):
    """Custom scene for preview canvas"""
    
    def __init__(self, width: int, height: int, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, width, height)
        
        # Background
        self.setBackgroundBrush(QBrush(QColor(20, 20, 20)))
        
        # Background image
        self.background_pixmap: Optional[QPixmap] = None
    
    def set_background(self, image_path: Optional[str]):
        """Set background image"""
        if image_path:
            self.background_pixmap = QPixmap(image_path).scaled(
                int(self.width()), 
                int(self.height()),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
        else:
            self.background_pixmap = None
        self.update()
    
    def drawBackground(self, painter: QPainter, rect: QRectF):
        """Draw background"""
        if self.background_pixmap:
            painter.drawPixmap(0, 0, self.background_pixmap)
        else:
            super().drawBackground(painter, rect)


class PreviewWidget(QWidget):
    """
    Preview widget with playback controls
    """
    
    time_changed = pyqtSignal(float)  # Emitted when playback position changes
    
    def __init__(self, audio_processor: AudioProcessor, project: ProjectState, parent=None):
        super().__init__(parent)
        self.audio_processor = audio_processor
        self.project = project
        
        # Playback state
        self.is_playing = False
        self.current_time = 0.0
        
        # Elements
        self.elements: List[DraggableElement] = []
        
        # Setup UI
        self.setup_ui()
        
        # Preview timer
        self.preview_timer = QTimer()
        self.preview_timer.timeout.connect(self.update_preview)
        self.preview_interval = 1000 // PREVIEW_FPS  # milliseconds
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Graphics view and scene
        self.scene = PreviewScene(
            self.project.resolution[0],
            self.project.resolution[1]
        )
        
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.view.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        
        # Playback controls
        controls_layout = QHBoxLayout()
        
        # Play/Pause button
        self.play_button = QPushButton("▶ Play")
        self.play_button.setFixedWidth(100)
        self.play_button.clicked.connect(self.toggle_playback)
        
        # Stop button
        self.stop_button = QPushButton("⏹ Stop")
        self.stop_button.setFixedWidth(80)
        self.stop_button.clicked.connect(self.stop_playback)
        
        # Timeline slider
        self.timeline_slider = QSlider(Qt.Orientation.Horizontal)
        self.timeline_slider.setMinimum(0)
        self.timeline_slider.setMaximum(1000)  # 0-1000 range
        self.timeline_slider.setValue(0)
        self.timeline_slider.sliderPressed.connect(self.on_slider_pressed)
        self.timeline_slider.sliderReleased.connect(self.on_slider_released)
        self.timeline_slider.sliderMoved.connect(self.on_slider_moved)
        
        # Time label
        self.time_label = QLabel("0:00 / 0:00")
        self.time_label.setFixedWidth(100)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.stop_button)
        controls_layout.addWidget(self.timeline_slider)
        controls_layout.addWidget(self.time_label)
        
        # Add to main layout
        layout.addWidget(self.view, stretch=1)
        layout.addLayout(controls_layout)
        
        # Update slider on audio load
        self.update_timeline()
    
    def add_element(self, element: DraggableElement):
        """Add element to preview"""
        self.elements.append(element)
        self.scene.addItem(element)
        element.setPos(element.state.x, element.state.y)
        element.setZValue(element.state.z_index)
    
    def clear_elements(self):
        """Clear all elements"""
        for element in self.elements:
            self.scene.removeItem(element)
        self.elements.clear()
    
    def set_background(self, image_path: Optional[str]):
        """Set background image"""
        self.scene.set_background(image_path)
        self.project.background_path = image_path
    
    def toggle_playback(self):
        """Toggle play/pause"""
        if self.is_playing:
            self.pause()
        else:
            self.play()
    
    def play(self):
        """Start playback"""
        if self.audio_processor.audio is None:
            return
        
        self.is_playing = True
        self.play_button.setText("⏸ Pause")
        
        # Start audio playback
        self.audio_processor.play(self.current_time)
        
        # Start preview timer
        self.preview_timer.start(self.preview_interval)
    
    def pause(self):
        """Pause playback"""
        self.is_playing = False
        self.play_button.setText("▶ Play")
        
        # Pause audio
        self.audio_processor.pause()
        
        # Stop preview timer
        self.preview_timer.stop()
    
    def stop_playback(self):
        """Stop playback and reset to beginning"""
        self.is_playing = False
        self.play_button.setText("▶ Play")
        
        # Stop audio
        self.audio_processor.stop()
        
        # Stop preview timer
        self.preview_timer.stop()
        
        # Reset time
        self.current_time = 0.0
        self.update_timeline()
        self.update_elements()
    
    def update_preview(self):
        """Update preview frame (called by timer)"""
        if not self.is_playing:
            return
        
        # Get current playback position from audio
        self.current_time = self.audio_processor.get_playback_position()
        
        # Check if reached end
        if self.current_time >= self.audio_processor.duration:
            self.stop_playback()
            return
        
        # Update timeline
        self.update_timeline()
        
        # Update all elements
        self.update_elements()
        
        # Emit signal
        self.time_changed.emit(self.current_time)
    
    def update_elements(self):
        """Update all elements for current time"""
        from elements.visualizer_element import VisualizerElement
        
        for element in self.elements:
            if isinstance(element, VisualizerElement):
                element.update_spectrum(self.current_time)
                element.update()
    
    def update_timeline(self):
        """Update timeline slider and label"""
        if self.audio_processor.duration > 0:
            # Update slider
            position = int((self.current_time / self.audio_processor.duration) * 1000)
            self.timeline_slider.blockSignals(True)
            self.timeline_slider.setValue(position)
            self.timeline_slider.blockSignals(False)
            
            # Update label
            current = self.format_time(self.current_time)
            total = self.format_time(self.audio_processor.duration)
            self.time_label.setText(f"{current} / {total}")
        else:
            self.time_label.setText("0:00 / 0:00")
    
    def on_slider_pressed(self):
        """Handle slider press"""
        # Pause playback while seeking
        if self.is_playing:
            self.audio_processor.pause()
    
    def on_slider_released(self):
        """Handle slider release"""
        # Resume playback if it was playing
        if self.is_playing:
            self.audio_processor.play(self.current_time)
    
    def on_slider_moved(self, value: int):
        """Handle slider movement"""
        if self.audio_processor.duration > 0:
            # Calculate new time position
            self.current_time = (value / 1000.0) * self.audio_processor.duration
            
            # Seek audio
            self.audio_processor.seek(self.current_time)
            
            # Update elements
            self.update_elements()
            
            # Update label
            self.update_timeline()
    
    @staticmethod
    def format_time(seconds: float) -> str:
        """Format time as MM:SS"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"
