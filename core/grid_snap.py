"""
Grid snapping and alignment tools
"""
from typing import Tuple, List
from dataclasses import dataclass


@dataclass
class GridSettings:
    """Grid configuration"""
    enabled: bool = False
    size: int = 10  # Grid spacing in pixels
    visible: bool = True
    color: Tuple[int, int, int] = (80, 80, 80)
    opacity: float = 0.3


class GridSnap:
    """
    Grid snapping utilities
    """
    
    def __init__(self, grid_size: int = 10):
        self.grid_size = grid_size
        self.enabled = False
    
    def snap_position(self, x: float, y: float) -> Tuple[float, float]:
        """Snap position to grid"""
        if not self.enabled:
            return (x, y)
        
        snapped_x = round(x / self.grid_size) * self.grid_size
        snapped_y = round(y / self.grid_size) * self.grid_size
        
        return (snapped_x, snapped_y)
    
    def snap_size(self, width: float, height: float) -> Tuple[float, float]:
        """Snap size to grid"""
        if not self.enabled:
            return (width, height)
        
        snapped_w = round(width / self.grid_size) * self.grid_size
        snapped_h = round(height / self.grid_size) * self.grid_size
        
        # Ensure minimum size
        snapped_w = max(self.grid_size, snapped_w)
        snapped_h = max(self.grid_size, snapped_h)
        
        return (snapped_w, snapped_h)
    
    def snap_rect(self, x: float, y: float, width: float, height: float) -> Tuple[float, float, float, float]:
        """Snap entire rectangle to grid"""
        snapped_x, snapped_y = self.snap_position(x, y)
        snapped_w, snapped_h = self.snap_size(width, height)
        return (snapped_x, snapped_y, snapped_w, snapped_h)


class AlignmentGuides:
    """
    Smart alignment guides (like Photoshop/Figma)
    """
    
    def __init__(self, snap_threshold: int = 5):
        self.snap_threshold = snap_threshold
        self.enabled = True
    
    def find_alignments(self, element_bounds: Tuple[float, float, float, float],
                       other_elements: List[Tuple[float, float, float, float]],
                       canvas_size: Tuple[int, int]) -> dict:
        """
        Find potential alignment positions
        
        Args:
            element_bounds: (x, y, width, height) of moving element
            other_elements: List of (x, y, width, height) for other elements
            canvas_size: (width, height) of canvas
            
        Returns:
            Dict with alignment suggestions
        """
        if not self.enabled:
            return {}
        
        x, y, w, h = element_bounds
        canvas_w, canvas_h = canvas_size
        
        # Calculate element edges
        left = x
        right = x + w
        top = y
        bottom = y + h
        center_x = x + w / 2
        center_y = y + h / 2
        
        alignments = {
            'vertical': [],    # Vertical guide lines
            'horizontal': [],  # Horizontal guide lines
            'snap_x': None,    # Suggested X snap position
            'snap_y': None,    # Suggested Y snap position
        }
        
        # Check canvas center alignment
        if abs(center_x - canvas_w / 2) < self.snap_threshold:
            alignments['vertical'].append(canvas_w / 2)
            alignments['snap_x'] = canvas_w / 2 - w / 2
        
        if abs(center_y - canvas_h / 2) < self.snap_threshold:
            alignments['horizontal'].append(canvas_h / 2)
            alignments['snap_y'] = canvas_h / 2 - h / 2
        
        # Check alignment with other elements
        for other_x, other_y, other_w, other_h in other_elements:
            other_left = other_x
            other_right = other_x + other_w
            other_top = other_y
            other_bottom = other_y + other_h
            other_center_x = other_x + other_w / 2
            other_center_y = other_y + other_h / 2
            
            # Vertical alignments
            if abs(left - other_left) < self.snap_threshold:
                alignments['vertical'].append(other_left)
                if alignments['snap_x'] is None:
                    alignments['snap_x'] = other_left
            
            if abs(right - other_right) < self.snap_threshold:
                alignments['vertical'].append(other_right)
                if alignments['snap_x'] is None:
                    alignments['snap_x'] = other_right - w
            
            if abs(center_x - other_center_x) < self.snap_threshold:
                alignments['vertical'].append(other_center_x)
                if alignments['snap_x'] is None:
                    alignments['snap_x'] = other_center_x - w / 2
            
            # Horizontal alignments
            if abs(top - other_top) < self.snap_threshold:
                alignments['horizontal'].append(other_top)
                if alignments['snap_y'] is None:
                    alignments['snap_y'] = other_top
            
            if abs(bottom - other_bottom) < self.snap_threshold:
                alignments['horizontal'].append(other_bottom)
                if alignments['snap_y'] is None:
                    alignments['snap_y'] = other_bottom - h
            
            if abs(center_y - other_center_y) < self.snap_threshold:
                alignments['horizontal'].append(other_center_y)
                if alignments['snap_y'] is None:
                    alignments['snap_y'] = other_center_y - h / 2
        
        # Remove duplicates
        alignments['vertical'] = list(set(alignments['vertical']))
        alignments['horizontal'] = list(set(alignments['horizontal']))
        
        return alignments


class DistributionTools:
    """
    Tools for distributing elements evenly
    """
    
    @staticmethod
    def distribute_horizontally(elements: List[Tuple[float, float, float, float]],
                               spacing: float = None) -> List[Tuple[float, float]]:
        """
        Distribute elements horizontally with even spacing
        
        Args:
            elements: List of (x, y, width, height)
            spacing: Fixed spacing between elements (None = auto)
            
        Returns:
            List of new (x, y) positions
        """
        if len(elements) < 2:
            return [(e[0], e[1]) for e in elements]
        
        # Sort by x position
        sorted_elements = sorted(enumerate(elements), key=lambda e: e[1][0])
        
        # Calculate spacing
        if spacing is None:
            first = sorted_elements[0][1]
            last = sorted_elements[-1][1]
            
            first_left = first[0]
            last_right = last[0] + last[2]
            
            total_width = sum(e[1][2] for e in sorted_elements)
            available_space = last_right - first_left - total_width
            
            spacing = available_space / (len(elements) - 1) if len(elements) > 1 else 0
        
        # Calculate new positions
        new_positions = [None] * len(elements)
        current_x = sorted_elements[0][1][0]
        
        for i, (original_idx, (x, y, w, h)) in enumerate(sorted_elements):
            new_positions[original_idx] = (current_x, y)
            current_x += w + spacing
        
        return new_positions
    
    @staticmethod
    def distribute_vertically(elements: List[Tuple[float, float, float, float]],
                            spacing: float = None) -> List[Tuple[float, float]]:
        """
        Distribute elements vertically with even spacing
        """
        if len(elements) < 2:
            return [(e[0], e[1]) for e in elements]
        
        # Sort by y position
        sorted_elements = sorted(enumerate(elements), key=lambda e: e[1][1])
        
        # Calculate spacing
        if spacing is None:
            first = sorted_elements[0][1]
            last = sorted_elements[-1][1]
            
            first_top = first[1]
            last_bottom = last[1] + last[3]
            
            total_height = sum(e[1][3] for e in sorted_elements)
            available_space = last_bottom - first_top - total_height
            
            spacing = available_space / (len(elements) - 1) if len(elements) > 1 else 0
        
        # Calculate new positions
        new_positions = [None] * len(elements)
        current_y = sorted_elements[0][1][1]
        
        for i, (original_idx, (x, y, w, h)) in enumerate(sorted_elements):
            new_positions[original_idx] = (x, current_y)
            current_y += h + spacing
        
        return new_positions
    
    @staticmethod
    def align_left(elements: List[Tuple[float, float, float, float]]) -> List[Tuple[float, float]]:
        """Align all elements to leftmost edge"""
        if not elements:
            return []
        
        min_x = min(e[0] for e in elements)
        return [(min_x, e[1]) for e in elements]
    
    @staticmethod
    def align_right(elements: List[Tuple[float, float, float, float]]) -> List[Tuple[float, float]]:
        """Align all elements to rightmost edge"""
        if not elements:
            return []
        
        max_right = max(e[0] + e[2] for e in elements)
        return [(max_right - e[2], e[1]) for e in elements]
    
    @staticmethod
    def align_top(elements: List[Tuple[float, float, float, float]]) -> List[Tuple[float, float]]:
        """Align all elements to top edge"""
        if not elements:
            return []
        
        min_y = min(e[1] for e in elements)
        return [(e[0], min_y) for e in elements]
    
    @staticmethod
    def align_bottom(elements: List[Tuple[float, float, float, float]]) -> List[Tuple[float, float]]:
        """Align all elements to bottom edge"""
        if not elements:
            return []
        
        max_bottom = max(e[1] + e[3] for e in elements)
        return [(e[0], max_bottom - e[3]) for e in elements]
    
    @staticmethod
    def align_center_horizontal(elements: List[Tuple[float, float, float, float]]) -> List[Tuple[float, float]]:
        """Align all elements horizontally centered"""
        if not elements:
            return []
        
        # Calculate average center
        centers = [e[0] + e[2] / 2 for e in elements]
        avg_center = sum(centers) / len(centers)
        
        return [(avg_center - e[2] / 2, e[1]) for e in elements]
    
    @staticmethod
    def align_center_vertical(elements: List[Tuple[float, float, float, float]]) -> List[Tuple[float, float]]:
        """Align all elements vertically centered"""
        if not elements:
            return []
        
        # Calculate average center
        centers = [e[1] + e[3] / 2 for e in elements]
        avg_center = sum(centers) / len(centers)
        
        return [(e[0], avg_center - e[3] / 2) for e in elements]
