"""
Keyboard shortcuts help dialog
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QTableWidget, QTableWidgetItem, QPushButton,
                              QTabWidget, QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ShortcutsDialog(QDialog):
    """
    Dialog showing all keyboard shortcuts
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Keyboard Shortcuts")
        self.setModal(False)
        self.resize(600, 500)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("⌨️ Keyboard Shortcuts")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Tabs for categories
        tabs = QTabWidget()
        
        # File operations
        file_tab = self.create_shortcuts_table([
            ("Ctrl+N", "New Project"),
            ("Ctrl+O", "Open Project"),
            ("Ctrl+S", "Save Project"),
            ("Ctrl+Shift+S", "Save Project As"),
            ("Ctrl+E", "Export Video"),
            ("Ctrl+Q", "Quit Application"),
        ])
        tabs.addTab(file_tab, "File")
        
        # Edit operations
        edit_tab = self.create_shortcuts_table([
            ("Ctrl+Z", "Undo"),
            ("Ctrl+Y", "Redo"),
            ("Ctrl+C", "Copy Element"),
            ("Ctrl+V", "Paste Element"),
            ("Ctrl+D", "Duplicate Element"),
            ("Delete", "Delete Selected Element"),
            ("Ctrl+A", "Select All Elements"),
            ("Escape", "Deselect All"),
        ])
        tabs.addTab(edit_tab, "Edit")
        
        # Playback controls
        playback_tab = self.create_shortcuts_table([
            ("Space", "Play/Pause"),
            ("Home", "Go to Start"),
            ("End", "Go to End"),
            ("←", "Step Back (1 frame)"),
            ("→", "Step Forward (1 frame)"),
            ("Shift+←", "Jump Back (1 second)"),
            ("Shift+→", "Jump Forward (1 second)"),
        ])
        tabs.addTab(playback_tab, "Playback")
        
        # Element manipulation
        element_tab = self.create_shortcuts_table([
            ("Arrow Keys", "Nudge Element (1px)"),
            ("Shift+Arrow", "Nudge Element (10px)"),
            ("Ctrl+Arrow", "Resize Element (1px)"),
            ("Ctrl+Shift+Arrow", "Resize Element (10px)"),
            ("Ctrl+L", "Lock/Unlock Element"),
            ("Ctrl+H", "Hide/Show Element"),
            ("[", "Send Backward"),
            ("]", "Bring Forward"),
            ("Ctrl+[", "Send to Back"),
            ("Ctrl+]", "Bring to Front"),
        ])
        tabs.addTab(element_tab, "Elements")
        
        # View controls
        view_tab = self.create_shortcuts_table([
            ("Ctrl+0", "Reset Zoom (100%)"),
            ("Ctrl++", "Zoom In"),
            ("Ctrl+-", "Zoom Out"),
            ("Ctrl+B", "Toggle Element Borders"),
            ("Ctrl+G", "Toggle Grid"),
            ("Ctrl+R", "Toggle Rulers"),
            ("F11", "Toggle Fullscreen"),
        ])
        tabs.addTab(view_tab, "View")
        
        # Add elements
        add_tab = self.create_shortcuts_table([
            ("Ctrl+Alt+V", "Add Visualizer"),
            ("Ctrl+Alt+T", "Add Text"),
            ("Ctrl+Alt+P", "Add Progress Bar"),
            ("Ctrl+Alt+L", "Add Lyrics"),
            ("Ctrl+Alt+I", "Add Logo"),
        ])
        tabs.addTab(add_tab, "Add")
        
        layout.addWidget(tabs)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
    
    def create_shortcuts_table(self, shortcuts: list) -> QWidget:
        """Create table widget for shortcuts"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Shortcut", "Action"])
        table.setRowCount(len(shortcuts))
        
        # Set column widths
        table.setColumnWidth(0, 150)
        table.setColumnWidth(1, 400)
        
        # Populate table
        for i, (shortcut, action) in enumerate(shortcuts):
            # Shortcut
            shortcut_item = QTableWidgetItem(shortcut)
            shortcut_item.setFlags(shortcut_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            shortcut_font = QFont()
            shortcut_font.setBold(True)
            shortcut_item.setFont(shortcut_font)
            table.setItem(i, 0, shortcut_item)
            
            # Action
            action_item = QTableWidgetItem(action)
            action_item.setFlags(action_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            table.setItem(i, 1, action_item)
        
        # Adjust row heights
        table.resizeRowsToContents()
        
        layout.addWidget(table)
        return widget


class KeyboardShortcutManager:
    """
    Manages keyboard shortcuts and their actions
    """
    
    def __init__(self):
        self.shortcuts = {}
        self.enabled = True
    
    def register(self, key_sequence: str, action_name: str, callback):
        """Register a keyboard shortcut"""
        self.shortcuts[key_sequence] = {
            'name': action_name,
            'callback': callback,
            'enabled': True
        }
    
    def unregister(self, key_sequence: str):
        """Unregister a shortcut"""
        if key_sequence in self.shortcuts:
            del self.shortcuts[key_sequence]
    
    def execute(self, key_sequence: str) -> bool:
        """Execute shortcut action if registered"""
        if not self.enabled:
            return False
        
        if key_sequence in self.shortcuts:
            shortcut = self.shortcuts[key_sequence]
            if shortcut['enabled']:
                shortcut['callback']()
                return True
        
        return False
    
    def enable_shortcut(self, key_sequence: str, enabled: bool = True):
        """Enable/disable specific shortcut"""
        if key_sequence in self.shortcuts:
            self.shortcuts[key_sequence]['enabled'] = enabled
    
    def get_all_shortcuts(self) -> dict:
        """Get all registered shortcuts"""
        return {k: v['name'] for k, v in self.shortcuts.items()}
