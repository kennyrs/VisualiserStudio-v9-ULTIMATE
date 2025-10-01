"""
Export dialog with progress tracking
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QProgressBar, QPushButton, QGroupBox, QComboBox,
                              QSpinBox, QTextEdit)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from models.project_state import ProjectState


class ExportDialog(QDialog):
    """
    Dialog for video export settings and progress
    """
    
    export_requested = pyqtSignal(dict)  # Export settings
    
    def __init__(self, project: ProjectState, parent=None):
        super().__init__(parent)
        self.project = project
        self.is_exporting = False
        
        self.setWindowTitle("Export Video")
        self.setModal(True)
        self.resize(500, 400)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        
        # Settings group
        settings_group = QGroupBox("Export Settings")
        settings_layout = QVBoxLayout()
        
        # Resolution
        res_row = QHBoxLayout()
        res_row.addWidget(QLabel("Resolution:"))
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems([
            "1920x1080 (1080p)",
            "1280x720 (720p)",
            "3840x2160 (4K)",
            "1080x1920 (Vertical - Instagram/TikTok)"
        ])
        res_row.addWidget(self.resolution_combo)
        settings_layout.addLayout(res_row)
        
        # FPS
        fps_row = QHBoxLayout()
        fps_row.addWidget(QLabel("Frame Rate:"))
        self.fps_spin = QSpinBox()
        self.fps_spin.setMinimum(24)
        self.fps_spin.setMaximum(60)
        self.fps_spin.setValue(self.project.fps)
        self.fps_spin.setSuffix(" fps")
        fps_row.addWidget(self.fps_spin)
        fps_row.addStretch()
        settings_layout.addLayout(fps_row)
        
        # Quality (CRF)
        quality_row = QHBoxLayout()
        quality_row.addWidget(QLabel("Quality (CRF):"))
        self.quality_spin = QSpinBox()
        self.quality_spin.setMinimum(15)
        self.quality_spin.setMaximum(28)
        self.quality_spin.setValue(self.project.crf)
        self.quality_spin.setToolTip("Lower = Better quality (15-17: High, 18-20: Good, 21-23: Medium)")
        quality_row.addWidget(self.quality_spin)
        
        self.quality_label = QLabel("(Good)")
        quality_row.addWidget(self.quality_label)
        self.quality_spin.valueChanged.connect(self.update_quality_label)
        
        quality_row.addStretch()
        settings_layout.addLayout(quality_row)
        
        # Encoding preset
        preset_row = QHBoxLayout()
        preset_row.addWidget(QLabel("Encoding:"))
        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            "ultrafast",
            "superfast", 
            "veryfast",
            "faster",
            "fast",
            "medium",
            "slow",
            "slower"
        ])
        self.preset_combo.setCurrentText("medium")
        self.preset_combo.setToolTip("Faster = Larger file, Slower = Smaller file")
        preset_row.addWidget(self.preset_combo)
        preset_row.addStretch()
        settings_layout.addLayout(preset_row)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Progress group
        self.progress_group = QGroupBox("Export Progress")
        progress_layout = QVBoxLayout()
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Ready to export")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_layout.addWidget(self.status_label)
        
        # Log output
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        self.log_text.setFont(QFont("Courier", 9))
        progress_layout.addWidget(self.log_text)
        
        self.progress_group.setLayout(progress_layout)
        self.progress_group.setVisible(False)
        layout.addWidget(self.progress_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.export_button = QPushButton("Start Export")
        self.export_button.clicked.connect(self.start_export)
        button_layout.addWidget(self.export_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        # Initial quality label
        self.update_quality_label()
    
    def update_quality_label(self):
        """Update quality description label"""
        crf = self.quality_spin.value()
        if crf <= 17:
            text = "(High Quality)"
        elif crf <= 20:
            text = "(Good Quality)"
        elif crf <= 23:
            text = "(Medium Quality)"
        else:
            text = "(Lower Quality)"
        self.quality_label.setText(text)
    
    def start_export(self):
        """Start export process"""
        if self.is_exporting:
            return
        
        # Get resolution
        res_text = self.resolution_combo.currentText()
        if "1920x1080" in res_text:
            resolution = (1920, 1080)
        elif "1280x720" in res_text:
            resolution = (1280, 720)
        elif "3840x2160" in res_text:
            resolution = (3840, 2160)
        elif "1080x1920" in res_text:
            resolution = (1080, 1920)
        else:
            resolution = (1920, 1080)
        
        # Collect settings
        settings = {
            'resolution': resolution,
            'fps': self.fps_spin.value(),
            'crf': self.quality_spin.value(),
            'preset': self.preset_combo.currentText()
        }
        
        # Show progress
        self.progress_group.setVisible(True)
        self.export_button.setEnabled(False)
        self.is_exporting = True
        
        # Emit signal
        self.export_requested.emit(settings)
    
    def update_progress(self, value: int):
        """Update progress bar"""
        self.progress_bar.setValue(value)
    
    def update_status(self, status: str):
        """Update status label"""
        self.status_label.setText(status)
        self.add_log(status)
    
    def add_log(self, message: str):
        """Add message to log"""
        self.log_text.append(message)
    
    def export_finished(self, output_path: str):
        """Handle export completion"""
        self.is_exporting = False
        self.update_status(f"✓ Export complete: {output_path}")
        self.progress_bar.setValue(100)
        self.export_button.setEnabled(True)
        self.export_button.setText("Close")
        self.export_button.clicked.disconnect()
        self.export_button.clicked.connect(self.accept)
    
    def export_error(self, error: str):
        """Handle export error"""
        self.is_exporting = False
        self.update_status(f"✗ Export failed: {error}")
        self.export_button.setEnabled(True)
        self.add_log(f"ERROR: {error}")
