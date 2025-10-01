"""
Media panel for loading audio, background, and logo
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                              QLabel, QLineEdit, QFileDialog, QGroupBox)
from PyQt6.QtCore import pyqtSignal


class MediaPanel(QWidget):
    """
    Panel for managing media files
    """
    
    audio_loaded = pyqtSignal(str)  # Emits audio file path
    background_loaded = pyqtSignal(str)  # Emits background image path
    background_removed = pyqtSignal()
    logo_loaded = pyqtSignal(str)
    logo_removed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Audio section
        audio_group = QGroupBox("🎵 Audio File")
        audio_layout = QVBoxLayout()
        
        audio_row = QHBoxLayout()
        self.audio_path_edit = QLineEdit()
        self.audio_path_edit.setReadOnly(True)
        self.audio_path_edit.setPlaceholderText("No audio file loaded...")
        
        self.browse_audio_btn = QPushButton("Browse")
        self.browse_audio_btn.clicked.connect(self.browse_audio)
        
        audio_row.addWidget(self.audio_path_edit)
        audio_row.addWidget(self.browse_audio_btn)
        audio_layout.addLayout(audio_row)
        
        audio_group.setLayout(audio_layout)
        layout.addWidget(audio_group)
        
        # Background section
        bg_group = QGroupBox("🖼️ Background Image")
        bg_layout = QVBoxLayout()
        
        bg_row = QHBoxLayout()
        self.bg_path_edit = QLineEdit()
        self.bg_path_edit.setReadOnly(True)
        self.bg_path_edit.setPlaceholderText("No background image...")
        
        self.browse_bg_btn = QPushButton("Browse")
        self.browse_bg_btn.clicked.connect(self.browse_background)
        
        self.remove_bg_btn = QPushButton("Remove")
        self.remove_bg_btn.clicked.connect(self.remove_background)
        self.remove_bg_btn.setEnabled(False)
        
        bg_row.addWidget(self.bg_path_edit)
        bg_row.addWidget(self.browse_bg_btn)
        bg_row.addWidget(self.remove_bg_btn)
        bg_layout.addLayout(bg_row)
        
        bg_group.setLayout(bg_layout)
        layout.addWidget(bg_group)
        
        # Logo section
        logo_group = QGroupBox("🏷️ Logo")
        logo_layout = QVBoxLayout()
        
        logo_row = QHBoxLayout()
        self.logo_path_edit = QLineEdit()
        self.logo_path_edit.setReadOnly(True)
        self.logo_path_edit.setPlaceholderText("No logo...")
        
        self.browse_logo_btn = QPushButton("Browse")
        self.browse_logo_btn.clicked.connect(self.browse_logo)
        
        self.remove_logo_btn = QPushButton("Remove")
        self.remove_logo_btn.clicked.connect(self.remove_logo)
        self.remove_logo_btn.setEnabled(False)
        
        logo_row.addWidget(self.logo_path_edit)
        logo_row.addWidget(self.browse_logo_btn)
        logo_row.addWidget(self.remove_logo_btn)
        logo_layout.addLayout(logo_row)
        
        logo_group.setLayout(logo_layout)
        layout.addWidget(logo_group)
        
        # Stretch at bottom
        layout.addStretch()
    
    def browse_audio(self):
        """Browse for audio file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            "",
            "Audio Files (*.mp3 *.wav *.ogg *.flac *.m4a);;All Files (*.*)"
        )
        
        if file_path:
            self.audio_path_edit.setText(file_path)
            self.audio_loaded.emit(file_path)
    
    def browse_background(self):
        """Browse for background image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Background Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*.*)"
        )
        
        if file_path:
            self.bg_path_edit.setText(file_path)
            self.remove_bg_btn.setEnabled(True)
            self.background_loaded.emit(file_path)
    
    def remove_background(self):
        """Remove background image"""
        self.bg_path_edit.clear()
        self.remove_bg_btn.setEnabled(False)
        self.background_removed.emit()
    
    def browse_logo(self):
        """Browse for logo image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Logo",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*.*)"
        )
        
        if file_path:
            self.logo_path_edit.setText(file_path)
            self.remove_logo_btn.setEnabled(True)
            self.logo_loaded.emit(file_path)
    
    def remove_logo(self):
        """Remove logo"""
        self.logo_path_edit.clear()
        self.remove_logo_btn.setEnabled(False)
        self.logo_removed.emit()
