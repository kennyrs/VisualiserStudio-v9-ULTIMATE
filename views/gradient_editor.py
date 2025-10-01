"""
Custom gradient editor dialog
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                              QLabel, QColorDialog, QListWidget, QSpinBox,
                              QSlider, QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QRectF
from PyQt6.QtGui import QPainter, QLinearGradient, QColor, QPen
from typing import List, Tuple


class GradientPreview(QListWidget):
    """Widget to preview gradient"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.colors: List[Tuple[int, int, int]] = []
        self.setFixedHeight(80)
        self.setFixedWidth(300)
    
    def set_colors(self, colors: List[Tuple[int, int, int]]):
        """Update gradient colors"""
        self.colors = colors
        self.update()
    
    def paintEvent(self, event):
        """Draw gradient preview"""
        if not self.colors:
            return super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        # Create linear gradient
        gradient = QLinearGradient(0, 0, width, 0)
        
        for i, color in enumerate(self.colors):
            position = i / (len(self.colors) - 1) if len(self.colors) > 1 else 0
            gradient.setColorAt(position, QColor(*color))
        
        # Draw gradient rectangle
        painter.fillRect(QRectF(0, 0, width, height), gradient)
        
        # Draw border
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.drawRect(QRectF(0, 0, width, height))
        
        painter.end()


class ColorStopWidget(QListWidget):
    """Widget for managing color stops"""
    
    stop_selected = pyqtSignal(int)  # Index of selected stop
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.colors: List[Tuple[int, int, int]] = []
        self.itemClicked.connect(self._on_item_clicked)
    
    def set_colors(self, colors: List[Tuple[int, int, int]]):
        """Update color stops list"""
        self.colors = colors
        self.clear()
        
        for i, color in enumerate(colors):
            r, g, b = color
            item_text = f"Stop {i+1}: RGB({r}, {g}, {b})"
            self.addItem(item_text)
    
    def _on_item_clicked(self, item):
        """Handle item click"""
        index = self.row(item)
        self.stop_selected.emit(index)


class GradientEditorDialog(QDialog):
    """
    Dialog for creating and editing custom gradients
    """
    
    gradient_created = pyqtSignal(str, list)  # name, colors
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.colors: List[Tuple[int, int, int]] = [(255, 0, 0), (0, 0, 255)]
        self.selected_stop = 0
        
        self.setWindowTitle("Gradient Editor")
        self.setModal(True)
        self.resize(400, 500)
        
        self.setup_ui()
        self.update_preview()
    
    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        
        # Name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Gradient Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("My Custom Gradient")
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Preview
        layout.addWidget(QLabel("Preview:"))
        self.preview = GradientPreview()
        layout.addWidget(self.preview)
        
        # Color stops
        layout.addWidget(QLabel("Color Stops:"))
        self.stops_widget = ColorStopWidget()
        self.stops_widget.stop_selected.connect(self.on_stop_selected)
        layout.addWidget(self.stops_widget)
        
        # Color stop controls
        controls_layout = QHBoxLayout()
        
        self.add_stop_btn = QPushButton("Add Stop")
        self.add_stop_btn.clicked.connect(self.add_color_stop)
        controls_layout.addWidget(self.add_stop_btn)
        
        self.remove_stop_btn = QPushButton("Remove Stop")
        self.remove_stop_btn.clicked.connect(self.remove_color_stop)
        controls_layout.addWidget(self.remove_stop_btn)
        
        self.edit_color_btn = QPushButton("Edit Color")
        self.edit_color_btn.clicked.connect(self.edit_color)
        controls_layout.addWidget(self.edit_color_btn)
        
        layout.addLayout(controls_layout)
        
        # RGB sliders for selected stop
        layout.addWidget(QLabel("Selected Stop Color:"))
        
        # Red
        red_layout = QHBoxLayout()
        red_layout.addWidget(QLabel("R:"))
        self.red_slider = QSlider(Qt.Orientation.Horizontal)
        self.red_slider.setMinimum(0)
        self.red_slider.setMaximum(255)
        self.red_slider.valueChanged.connect(self.on_rgb_changed)
        red_layout.addWidget(self.red_slider)
        self.red_label = QLabel("0")
        red_layout.addWidget(self.red_label)
        layout.addLayout(red_layout)
        
        # Green
        green_layout = QHBoxLayout()
        green_layout.addWidget(QLabel("G:"))
        self.green_slider = QSlider(Qt.Orientation.Horizontal)
        self.green_slider.setMinimum(0)
        self.green_slider.setMaximum(255)
        self.green_slider.valueChanged.connect(self.on_rgb_changed)
        green_layout.addWidget(self.green_slider)
        self.green_label = QLabel("0")
        green_layout.addWidget(self.green_label)
        layout.addLayout(green_layout)
        
        # Blue
        blue_layout = QHBoxLayout()
        blue_layout.addWidget(QLabel("B:"))
        self.blue_slider = QSlider(Qt.Orientation.Horizontal)
        self.blue_slider.setMinimum(0)
        self.blue_slider.setMaximum(255)
        self.blue_slider.valueChanged.connect(self.on_rgb_changed)
        blue_layout.addWidget(self.blue_slider)
        self.blue_label = QLabel("0")
        blue_layout.addWidget(self.blue_label)
        layout.addLayout(blue_layout)
        
        # Preset buttons
        layout.addWidget(QLabel("Quick Presets:"))
        presets_layout = QHBoxLayout()
        
        presets = [
            ("Warm Sunset", [(255, 94, 77), (255, 165, 100), (255, 206, 128)]),
            ("Cool Ocean", [(0, 119, 190), (0, 180, 216), (72, 202, 228)]),
            ("Neon Party", [(0, 255, 255), (255, 0, 255), (255, 255, 0)]),
            ("Forest", [(34, 139, 34), (50, 205, 50), (144, 238, 144)])
        ]
        
        for name, colors in presets:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, c=colors: self.load_preset(c))
            presets_layout.addWidget(btn)
        
        layout.addLayout(presets_layout)
        
        # Dialog buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        self.save_btn = QPushButton("Save Gradient")
        self.save_btn.clicked.connect(self.save_gradient)
        buttons_layout.addWidget(self.save_btn)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        # Initial selection
        self.select_stop(0)
    
    def update_preview(self):
        """Update gradient preview"""
        self.preview.set_colors(self.colors)
        self.stops_widget.set_colors(self.colors)
    
    def select_stop(self, index: int):
        """Select a color stop"""
        if 0 <= index < len(self.colors):
            self.selected_stop = index
            r, g, b = self.colors[index]
            
            # Update sliders
            self.red_slider.blockSignals(True)
            self.green_slider.blockSignals(True)
            self.blue_slider.blockSignals(True)
            
            self.red_slider.setValue(r)
            self.green_slider.setValue(g)
            self.blue_slider.setValue(b)
            
            self.red_label.setText(str(r))
            self.green_label.setText(str(g))
            self.blue_label.setText(str(b))
            
            self.red_slider.blockSignals(False)
            self.green_slider.blockSignals(False)
            self.blue_slider.blockSignals(False)
    
    def on_stop_selected(self, index: int):
        """Handle stop selection"""
        self.select_stop(index)
    
    def on_rgb_changed(self):
        """Handle RGB slider change"""
        if 0 <= self.selected_stop < len(self.colors):
            r = self.red_slider.value()
            g = self.green_slider.value()
            b = self.blue_slider.value()
            
            self.colors[self.selected_stop] = (r, g, b)
            
            self.red_label.setText(str(r))
            self.green_label.setText(str(g))
            self.blue_label.setText(str(b))
            
            self.update_preview()
    
    def add_color_stop(self):
        """Add new color stop"""
        if len(self.colors) >= 10:
            QMessageBox.warning(self, "Limit Reached", "Maximum 10 color stops allowed")
            return
        
        # Add between current and next stop
        if self.selected_stop < len(self.colors) - 1:
            color1 = self.colors[self.selected_stop]
            color2 = self.colors[self.selected_stop + 1]
            
            # Interpolate
            new_color = (
                (color1[0] + color2[0]) // 2,
                (color1[1] + color2[1]) // 2,
                (color1[2] + color2[2]) // 2
            )
            
            self.colors.insert(self.selected_stop + 1, new_color)
        else:
            # Add at end
            self.colors.append((255, 255, 255))
        
        self.update_preview()
    
    def remove_color_stop(self):
        """Remove selected color stop"""
        if len(self.colors) <= 2:
            QMessageBox.warning(self, "Cannot Remove", "Gradient must have at least 2 colors")
            return
        
        if 0 <= self.selected_stop < len(self.colors):
            self.colors.pop(self.selected_stop)
            
            # Adjust selection
            if self.selected_stop >= len(self.colors):
                self.selected_stop = len(self.colors) - 1
            
            self.select_stop(self.selected_stop)
            self.update_preview()
    
    def edit_color(self):
        """Open color picker for selected stop"""
        if 0 <= self.selected_stop < len(self.colors):
            current_color = QColor(*self.colors[self.selected_stop])
            color = QColorDialog.getColor(current_color, self, "Choose Color")
            
            if color.isValid():
                self.colors[self.selected_stop] = (color.red(), color.green(), color.blue())
                self.select_stop(self.selected_stop)
                self.update_preview()
    
    def load_preset(self, colors: List[Tuple[int, int, int]]):
        """Load preset gradient"""
        self.colors = colors.copy()
        self.selected_stop = 0
        self.select_stop(0)
        self.update_preview()
    
    def save_gradient(self):
        """Save custom gradient"""
        name = self.name_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Name Required", "Please enter a name for the gradient")
            return
        
        if len(self.colors) < 2:
            QMessageBox.warning(self, "Invalid Gradient", "Gradient must have at least 2 colors")
            return
        
        self.gradient_created.emit(name, self.colors)
        self.accept()
