"""
Visualizer settings panel - COMPLETE v9.0 ULTIMATE
Supports all 12 visualizer types + advanced features
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QComboBox, QSlider, QSpinBox, QCheckBox, 
                              QGroupBox, QPushButton)
from PyQt6.QtCore import Qt, pyqtSignal

from models.project_state import VisualizerSettings
from utils.config import VisualizerType, GRADIENTS


class VisualizerPanel(QWidget):
    """
    Panel for visualizer settings with all 12 types
    """
    
    settings_changed = pyqtSignal(VisualizerSettings)
    add_visualizer_clicked = pyqtSignal()
    open_gradient_editor = pyqtSignal()
    
    def __init__(self, settings: VisualizerSettings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Add visualizer button
        self.add_viz_btn = QPushButton("➕ Add Visualizer")
        self.add_viz_btn.clicked.connect(self.add_visualizer_clicked.emit)
        self.add_viz_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        layout.addWidget(self.add_viz_btn)
        
        # Type and style
        style_group = QGroupBox("Style")
        style_layout = QVBoxLayout()
        
        # Visualizer type (ALL 12 TYPES)
        type_row = QHBoxLayout()
        type_row.addWidget(QLabel("Type:"))
        self.type_combo = QComboBox()
        
        # Add all visualizer types
        viz_types = [
            ("BARS", "Classic Equalizer"),
            ("MIRROR_BARS", "Symmetric Mirror"),
            ("LINE", "Smooth Wave Line"),
            ("AREA", "Filled Area"),
            ("CIRCULAR", "360° Radial"),
            ("RING", "Pulsing Ring"),
            ("DOTS", "Particle System"),
            ("WAVEFORM", "Audio Waveform"),
            ("PIXEL_EQ", "Retro 8-bit"),
            ("RIBBON", "Flowing Ribbon"),
            ("SPIRAL", "Helix Spiral"),
            ("PULSE_CIRCLE", "Concentric Circles")
        ]
        
        for viz_id, viz_name in viz_types:
            self.type_combo.addItem(viz_name, VisualizerType[viz_id])
        
        self.type_combo.currentIndexChanged.connect(self.on_type_changed)
        type_row.addWidget(self.type_combo)
        style_layout.addLayout(type_row)
        
        # Gradient
        gradient_row = QHBoxLayout()
        gradient_row.addWidget(QLabel("Gradient:"))
        self.gradient_combo = QComboBox()
        for gradient_name in GRADIENTS.keys():
            self.gradient_combo.addItem(gradient_name)
        self.gradient_combo.currentTextChanged.connect(self.on_settings_changed)
        gradient_row.addWidget(self.gradient_combo)
        
        # Custom gradient button
        self.custom_gradient_btn = QPushButton("✏️")
        self.custom_gradient_btn.setToolTip("Open Gradient Editor")
        self.custom_gradient_btn.setFixedWidth(40)
        self.custom_gradient_btn.clicked.connect(self.open_gradient_editor.emit)
        gradient_row.addWidget(self.custom_gradient_btn)
        
        style_layout.addLayout(gradient_row)
        
        style_group.setLayout(style_layout)
        layout.addWidget(style_group)
        
        # Parameters
        params_group = QGroupBox("Parameters")
        params_layout = QVBoxLayout()
        
        # EQ Bands
        bands_row = QHBoxLayout()
        bands_row.addWidget(QLabel("EQ Bands:"))
        self.bands_spin = QSpinBox()
        self.bands_spin.setMinimum(8)
        self.bands_spin.setMaximum(64)
        self.bands_spin.setValue(20)
        self.bands_spin.valueChanged.connect(self.on_settings_changed)
        bands_row.addWidget(self.bands_spin)
        bands_row.addStretch()
        params_layout.addLayout(bands_row)
        
        # Smoothness
        smooth_row = QHBoxLayout()
        smooth_row.addWidget(QLabel("Smoothness:"))
        self.smooth_slider = QSlider(Qt.Orientation.Horizontal)
        self.smooth_slider.setMinimum(0)
        self.smooth_slider.setMaximum(100)
        self.smooth_slider.setValue(70)
        self.smooth_slider.valueChanged.connect(self.on_settings_changed)
        self.smooth_label = QLabel("0.70")
        self.smooth_label.setMinimumWidth(40)
        smooth_row.addWidget(self.smooth_slider)
        smooth_row.addWidget(self.smooth_label)
        params_layout.addLayout(smooth_row)
        
        # Line thickness (for LINE, WAVEFORM, etc.)
        thickness_row = QHBoxLayout()
        thickness_row.addWidget(QLabel("Line Thickness:"))
        self.thickness_spin = QSpinBox()
        self.thickness_spin.setMinimum(1)
        self.thickness_spin.setMaximum(10)
        self.thickness_spin.setValue(3)
        self.thickness_spin.valueChanged.connect(self.on_settings_changed)
        thickness_row.addWidget(self.thickness_spin)
        thickness_row.addStretch()
        params_layout.addLayout(thickness_row)
        
        # Rounded bars checkbox
        self.rounded_check = QCheckBox("Rounded Bars")
        self.rounded_check.setChecked(True)
        self.rounded_check.stateChanged.connect(self.on_settings_changed)
        params_layout.addWidget(self.rounded_check)
        
        # Mirror gap (for MIRROR_BARS)
        gap_row = QHBoxLayout()
        gap_row.addWidget(QLabel("Mirror Gap:"))
        self.gap_spin = QSpinBox()
        self.gap_spin.setMinimum(0)
        self.gap_spin.setMaximum(100)
        self.gap_spin.setValue(20)
        self.gap_spin.valueChanged.connect(self.on_settings_changed)
        gap_row.addWidget(self.gap_spin)
        gap_row.addStretch()
        params_layout.addLayout(gap_row)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # Effects
        effects_group = QGroupBox("Effects")
        effects_layout = QVBoxLayout()
        
        # Glow checkbox
        self.glow_check = QCheckBox("Enable Glow Effect")
        self.glow_check.setChecked(False)
        self.glow_check.stateChanged.connect(self.on_settings_changed)
        effects_layout.addWidget(self.glow_check)
        
        # Glow blur
        blur_row = QHBoxLayout()
        blur_row.addWidget(QLabel("  Blur Size:"))
        self.blur_spin = QSpinBox()
        self.blur_spin.setMinimum(1)
        self.blur_spin.setMaximum(101)
        self.blur_spin.setSingleStep(2)
        self.blur_spin.setValue(31)
        self.blur_spin.valueChanged.connect(self.on_blur_changed)
        blur_row.addWidget(self.blur_spin)
        blur_row.addStretch()
        effects_layout.addLayout(blur_row)
        
        # Glow intensity
        intensity_row = QHBoxLayout()
        intensity_row.addWidget(QLabel("  Intensity:"))
        self.intensity_slider = QSlider(Qt.Orientation.Horizontal)
        self.intensity_slider.setMinimum(0)
        self.intensity_slider.setMaximum(100)
        self.intensity_slider.setValue(50)
        self.intensity_slider.valueChanged.connect(self.on_settings_changed)
        self.intensity_label = QLabel("0.50")
        self.intensity_label.setMinimumWidth(40)
        intensity_row.addWidget(self.intensity_slider)
        intensity_row.addWidget(self.intensity_label)
        effects_layout.addLayout(intensity_row)
        
        effects_group.setLayout(effects_layout)
        layout.addWidget(effects_group)
        
        # Presets section
        presets_group = QGroupBox("Quick Presets")
        presets_layout = QVBoxLayout()
        
        presets_info = QLabel("Apply quick settings for different music genres:")
        presets_info.setWordWrap(True)
        presets_layout.addWidget(presets_info)
        
        # Preset buttons
        preset_row1 = QHBoxLayout()
        
        edm_btn = QPushButton("EDM")
        edm_btn.clicked.connect(lambda: self.apply_preset("edm"))
        preset_row1.addWidget(edm_btn)
        
        chill_btn = QPushButton("Chill")
        chill_btn.clicked.connect(lambda: self.apply_preset("chill"))
        preset_row1.addWidget(chill_btn)
        
        presets_layout.addLayout(preset_row1)
        
        preset_row2 = QHBoxLayout()
        
        rock_btn = QPushButton("Rock")
        rock_btn.clicked.connect(lambda: self.apply_preset("rock"))
        preset_row2.addWidget(rock_btn)
        
        classical_btn = QPushButton("Classical")
        classical_btn.clicked.connect(lambda: self.apply_preset("classical"))
        preset_row2.addWidget(classical_btn)
        
        presets_layout.addLayout(preset_row2)
        
        presets_group.setLayout(presets_layout)
        layout.addWidget(presets_group)
        
        # Stretch at bottom
        layout.addStretch()
    
    def load_settings(self):
        """Load current settings into UI"""
        # Find index of visualizer type
        for i in range(self.type_combo.count()):
            if self.type_combo.itemData(i) == self.settings.visualizer_type:
                self.type_combo.setCurrentIndex(i)
                break
        
        # Set gradient
        index = self.gradient_combo.findText(self.settings.gradient)
        if index >= 0:
            self.gradient_combo.setCurrentIndex(index)
        
        # Set parameters
        self.bands_spin.setValue(self.settings.eq_bands)
        self.smooth_slider.setValue(int(self.settings.smoothness * 100))
        self.thickness_spin.setValue(self.settings.line_thickness)
        self.rounded_check.setChecked(self.settings.rounded_bars)
        self.gap_spin.setValue(self.settings.mirror_gap)
        
        # Set effects
        self.glow_check.setChecked(self.settings.glow_enabled)
        self.blur_spin.setValue(self.settings.glow_blur)
        self.intensity_slider.setValue(int(self.settings.glow_intensity * 100))
        
        # Update labels
        self.update_labels()
    
    def on_type_changed(self):
        """Handle visualizer type change"""
        self.on_settings_changed()
        
        # Show/hide relevant controls based on type
        viz_type = self.type_combo.currentData()
        
        # Line thickness only for LINE, WAVEFORM
        show_thickness = viz_type in [VisualizerType.LINE, VisualizerType.WAVEFORM]
        self.thickness_spin.setEnabled(show_thickness)
        
        # Rounded bars only for BARS, MIRROR_BARS
        show_rounded = viz_type in [VisualizerType.BARS, VisualizerType.MIRROR_BARS]
        self.rounded_check.setEnabled(show_rounded)
        
        # Mirror gap only for MIRROR_BARS
        show_gap = viz_type == VisualizerType.MIRROR_BARS
        self.gap_spin.setEnabled(show_gap)
    
    def on_blur_changed(self, value):
        """Ensure blur size is odd"""
        if value % 2 == 0:
            self.blur_spin.setValue(value + 1)
        else:
            self.on_settings_changed()
    
    def on_settings_changed(self):
        """Handle any settings change"""
        # Update settings object
        self.settings.visualizer_type = self.type_combo.currentData()
        self.settings.gradient = self.gradient_combo.currentText()
        self.settings.eq_bands = self.bands_spin.value()
        self.settings.smoothness = self.smooth_slider.value() / 100.0
        self.settings.line_thickness = self.thickness_spin.value()
        self.settings.rounded_bars = self.rounded_check.isChecked()
        self.settings.mirror_gap = self.gap_spin.value()
        self.settings.glow_enabled = self.glow_check.isChecked()
        self.settings.glow_blur = self.blur_spin.value()
        self.settings.glow_intensity = self.intensity_slider.value() / 100.0
        
        # Update labels
        self.update_labels()
        
        # Emit signal
        self.settings_changed.emit(self.settings)
    
    def update_labels(self):
        """Update numeric labels"""
        self.smooth_label.setText(f"{self.settings.smoothness:.2f}")
        self.intensity_label.setText(f"{self.settings.glow_intensity:.2f}")
    
    def apply_preset(self, preset_name: str):
        """Apply preset configuration"""
        presets = {
            "edm": {
                "type": VisualizerType.MIRROR_BARS,
                "gradient": "Neon",
                "bands": 32,
                "smoothness": 0.6,
                "glow": True
            },
            "chill": {
                "type": VisualizerType.LINE,
                "gradient": "Ocean",
                "bands": 20,
                "smoothness": 0.85,
                "glow": False
            },
            "rock": {
                "type": VisualizerType.BARS,
                "gradient": "Fire",
                "bands": 24,
                "smoothness": 0.65,
                "glow": True
            },
            "classical": {
                "type": VisualizerType.AREA,
                "gradient": "Purple",
                "bands": 16,
                "smoothness": 0.9,
                "glow": False
            }
        }
        
        if preset_name in presets:
            preset = presets[preset_name]
            
            # Set visualizer type
            for i in range(self.type_combo.count()):
                if self.type_combo.itemData(i) == preset["type"]:
                    self.type_combo.setCurrentIndex(i)
                    break
            
            # Set gradient
            index = self.gradient_combo.findText(preset["gradient"])
            if index >= 0:
                self.gradient_combo.setCurrentIndex(index)
            
            # Set parameters
            self.bands_spin.setValue(preset["bands"])
            self.smooth_slider.setValue(int(preset["smoothness"] * 100))
            self.glow_check.setChecked(preset["glow"])
            
            # Trigger update
            self.on_settings_changed()