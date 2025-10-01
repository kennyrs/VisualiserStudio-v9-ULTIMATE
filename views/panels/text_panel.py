"""
Text settings panel
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QTextEdit, QComboBox, QSlider, QSpinBox, 
                              QCheckBox, QPushButton, QGroupBox, QColorDialog)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont

from models.project_state import TextSettings


class TextPanel(QWidget):
    """
    Panel for text settings
    """
    
    settings_changed = pyqtSignal(TextSettings)
    add_text_clicked = pyqtSignal()
    
    def __init__(self, settings: TextSettings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Add text button
        self.add_text_btn = QPushButton("➕ Add Text")
        self.add_text_btn.clicked.connect(self.add_text_clicked.emit)
        layout.addWidget(self.add_text_btn)
        
        # Content
        content_group = QGroupBox("Content")
        content_layout = QVBoxLayout()
        
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("Enter text here...")
        self.content_edit.setMaximumHeight(100)
        self.content_edit.textChanged.connect(self.on_settings_changed)
        content_layout.addWidget(self.content_edit)
        
        # Quick templates
        templates_row = QHBoxLayout()
        templates_row.addWidget(QLabel("Templates:"))
        
        self.template_combo = QComboBox()
        self.template_combo.addItems([
            "Custom",
            "Song - Artist",
            "Artist Name",
            "Song Title"
        ])
        self.template_combo.currentTextChanged.connect(self.on_template_selected)
        templates_row.addWidget(self.template_combo)
        content_layout.addLayout(templates_row)
        
        content_group.setLayout(content_layout)
        layout.addWidget(content_group)
        
        # Font settings
        font_group = QGroupBox("Font")
        font_layout = QVBoxLayout()
        
        # Font family
        family_row = QHBoxLayout()
        family_row.addWidget(QLabel("Font:"))
        self.font_combo = QComboBox()
        
        # Add common fonts
        fonts = [
            "Arial", "Arial Black", "Comic Sans MS", "Courier New",
            "Georgia", "Impact", "Times New Roman", "Trebuchet MS",
            "Verdana"
        ]
        self.font_combo.addItems(fonts)
        self.font_combo.currentTextChanged.connect(self.on_settings_changed)
        family_row.addWidget(self.font_combo)
        font_layout.addLayout(family_row)
        
        # Font size
        size_row = QHBoxLayout()
        size_row.addWidget(QLabel("Size:"))
        self.size_spin = QSpinBox()
        self.size_spin.setMinimum(12)
        self.size_spin.setMaximum(200)
        self.size_spin.setValue(72)
        self.size_spin.valueChanged.connect(self.on_settings_changed)
        size_row.addWidget(self.size_spin)
        
        self.size_slider = QSlider(Qt.Orientation.Horizontal)
        self.size_slider.setMinimum(12)
        self.size_slider.setMaximum(200)
        self.size_slider.setValue(72)
        self.size_slider.valueChanged.connect(self.size_spin.setValue)
        self.size_spin.valueChanged.connect(self.size_slider.setValue)
        size_row.addWidget(self.size_slider)
        font_layout.addLayout(size_row)
        
        # Bold checkbox
        self.bold_check = QCheckBox("Bold")
        self.bold_check.setChecked(True)
        self.bold_check.stateChanged.connect(self.on_settings_changed)
        font_layout.addWidget(self.bold_check)
        
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        # Color
        color_group = QGroupBox("Color")
        color_layout = QHBoxLayout()
        
        self.color_btn = QPushButton("Choose Color")
        self.color_btn.clicked.connect(self.choose_color)
        color_layout.addWidget(self.color_btn)
        
        self.color_preview = QWidget()
        self.color_preview.setFixedSize(50, 30)
        self.color_preview.setStyleSheet("background-color: white; border: 1px solid black;")
        color_layout.addWidget(self.color_preview)
        
        color_layout.addStretch()
        color_group.setLayout(color_layout)
        layout.addWidget(color_group)
        
        # Stretch at bottom
        layout.addStretch()
    
    def load_settings(self):
        """Load current settings into UI"""
        self.content_edit.setPlainText(self.settings.content)
        
        # Font family
        index = self.font_combo.findText(self.settings.font_family)
        if index >= 0:
            self.font_combo.setCurrentIndex(index)
        
        # Font size
        self.size_spin.setValue(self.settings.font_size)
        
        # Bold
        self.bold_check.setChecked(self.settings.bold)
        
        # Color
        self.update_color_preview()
    
    def on_settings_changed(self):
        """Handle any settings change"""
        self.settings.content = self.content_edit.toPlainText()
        self.settings.font_family = self.font_combo.currentText()
        self.settings.font_size = self.size_spin.value()
        self.settings.bold = self.bold_check.isChecked()
        
        # Emit signal
        self.settings_changed.emit(self.settings)
    
    def on_template_selected(self, template: str):
        """Handle template selection"""
        if template == "Song - Artist":
            self.content_edit.setPlainText("Song Title - Artist Name")
        elif template == "Artist Name":
            self.content_edit.setPlainText("Artist Name")
        elif template == "Song Title":
            self.content_edit.setPlainText("Song Title")
        # Custom = do nothing
    
    def choose_color(self):
        """Open color picker dialog"""
        current_color = QColor(*self.settings.color)
        color = QColorDialog.getColor(current_color, self, "Choose Text Color")
        
        if color.isValid():
            self.settings.color = (color.red(), color.green(), color.blue())
            self.update_color_preview()
            self.settings_changed.emit(self.settings)
    
    def update_color_preview(self):
        """Update color preview widget"""
        r, g, b = self.settings.color
        self.color_preview.setStyleSheet(
            f"background-color: rgb({r}, {g}, {b}); border: 1px solid black;"
        )
