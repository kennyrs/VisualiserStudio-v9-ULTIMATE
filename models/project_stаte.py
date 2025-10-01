"""
Data models for project state management
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Tuple, Dict, Any
from enum import Enum
import json

from utils.config import ElementType, VisualizerType


@dataclass
class ElementState:
    """State of a single UI element"""
    element_type: ElementType
    x: float
    y: float
    width: float
    height: float
    z_index: int = 0
    visible: bool = True
    locked: bool = False
    
    # Element-specific properties
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['element_type'] = self.element_type.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ElementState':
        """Create from dictionary"""
        data['element_type'] = ElementType(data['element_type'])
        return cls(**data)


@dataclass
class VisualizerSettings:
    """Settings specific to visualizer elements"""
    visualizer_type: VisualizerType = VisualizerType.BARS
    eq_bands: int = 20
    gradient: str = "Ocean"
    smoothness: float = 0.7
    line_thickness: int = 3
    rounded_bars: bool = True
    mirror_gap: int = 20
    glow_enabled: bool = False
    glow_blur: int = 31
    glow_intensity: float = 0.5
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['visualizer_type'] = self.visualizer_type.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'VisualizerSettings':
        data['visualizer_type'] = VisualizerType(data['visualizer_type'])
        return cls(**data)


@dataclass
class TextSettings:
    """Settings for text elements"""
    content: str = ""
    font_family: str = "Arial"
    font_size: int = 72
    bold: bool = True
    color: Tuple[int, int, int] = (255, 255, 255)
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TextSettings':
        return cls(**data)


@dataclass
class ProjectState:
    """Complete project state"""
    # Media files
    audio_path: Optional[str] = None
    background_path: Optional[str] = None
    logo_path: Optional[str] = None
    lyrics_path: Optional[str] = None
    
    # Elements
    elements: List[ElementState] = field(default_factory=list)
    
    # Export settings
    resolution: Tuple[int, int] = (1920, 1080)
    fps: int = 30
    crf: int = 18
    
    # Global settings
    visualizer_settings: VisualizerSettings = field(default_factory=VisualizerSettings)
    text_settings: TextSettings = field(default_factory=TextSettings)
    
    def save_to_file(self, filepath: str):
        """Save project to JSON file"""
        data = {
            'audio_path': self.audio_path,
            'background_path': self.background_path,
            'logo_path': self.logo_path,
            'lyrics_path': self.lyrics_path,
            'elements': [e.to_dict() for e in self.elements],
            'resolution': list(self.resolution),
            'fps': self.fps,
            'crf': self.crf,
            'visualizer_settings': self.visualizer_settings.to_dict(),
            'text_settings': self.text_settings.to_dict(),
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'ProjectState':
        """Load project from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        project = cls(
            audio_path=data.get('audio_path'),
            background_path=data.get('background_path'),
            logo_path=data.get('logo_path'),
            lyrics_path=data.get('lyrics_path'),
            resolution=tuple(data.get('resolution', [1920, 1080])),
            fps=data.get('fps', 30),
            crf=data.get('crf', 18),
        )
        
        # Load elements
        project.elements = [
            ElementState.from_dict(e) for e in data.get('elements', [])
        ]
        
        # Load settings
        if 'visualizer_settings' in data:
            project.visualizer_settings = VisualizerSettings.from_dict(
                data['visualizer_settings']
            )
        if 'text_settings' in data:
            project.text_settings = TextSettings.from_dict(
                data['text_settings']
            )
        
        return project
    
    def add_element(self, element: ElementState):
        """Add new element to project"""
        self.elements.append(element)
        self._update_z_indices()
    
    def remove_element(self, element: ElementState):
        """Remove element from project"""
        self.elements.remove(element)
        self._update_z_indices()
    
    def _update_z_indices(self):
        """Update z-indices after changes"""
        for i, element in enumerate(self.elements):
            element.z_index = i
