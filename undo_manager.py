"""
Undo/Redo system for all operations
"""
from dataclasses import dataclass, field
from typing import Any, List, Callable, Optional
from enum import Enum
import copy


class ActionType(Enum):
    """Types of undoable actions"""
    ADD_ELEMENT = "add_element"
    REMOVE_ELEMENT = "remove_element"
    MOVE_ELEMENT = "move_element"
    RESIZE_ELEMENT = "resize_element"
    MODIFY_PROPERTY = "modify_property"
    CHANGE_SETTINGS = "change_settings"


@dataclass
class UndoAction:
    """Single undoable action"""
    action_type: ActionType
    description: str
    
    # State before action
    before_state: Any
    
    # State after action
    after_state: Any
    
    # Target object/element identifier
    target_id: Optional[str] = None
    
    # Custom undo/redo functions
    undo_func: Optional[Callable] = None
    redo_func: Optional[Callable] = None
    
    def __repr__(self):
        return f"<UndoAction: {self.description}>"


class UndoManager:
    """
    Manages undo/redo stack with history
    """
    
    def __init__(self, max_history: int = 50):
        self.max_history = max_history
        self.undo_stack: List[UndoAction] = []
        self.redo_stack: List[UndoAction] = []
        
        self.is_performing_undo = False
        self.is_performing_redo = False
    
    def push(self, action: UndoAction):
        """Add action to undo stack"""
        if self.is_performing_undo or self.is_performing_redo:
            return
        
        self.undo_stack.append(action)
        
        # Limit stack size
        if len(self.undo_stack) > self.max_history:
            self.undo_stack.pop(0)
        
        # Clear redo stack when new action is performed
        self.redo_stack.clear()
    
    def can_undo(self) -> bool:
        """Check if undo is available"""
        return len(self.undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is available"""
        return len(self.redo_stack) > 0
    
    def undo(self) -> Optional[UndoAction]:
        """Perform undo"""
        if not self.can_undo():
            return None
        
        action = self.undo_stack.pop()
        
        self.is_performing_undo = True
        
        # Execute undo
        if action.undo_func:
            action.undo_func(action.before_state)
        
        self.is_performing_undo = False
        
        # Move to redo stack
        self.redo_stack.append(action)
        
        return action
    
    def redo(self) -> Optional[UndoAction]:
        """Perform redo"""
        if not self.can_redo():
            return None
        
        action = self.redo_stack.pop()
        
        self.is_performing_redo = True
        
        # Execute redo
        if action.redo_func:
            action.redo_func(action.after_state)
        
        self.is_performing_redo = False
        
        # Move back to undo stack
        self.undo_stack.append(action)
        
        return action
    
    def clear(self):
        """Clear all history"""
        self.undo_stack.clear()
        self.redo_stack.clear()
    
    def get_undo_description(self) -> str:
        """Get description of next undo action"""
        if self.can_undo():
            return self.undo_stack[-1].description
        return ""
    
    def get_redo_description(self) -> str:
        """Get description of next redo action"""
        if self.can_redo():
            return self.redo_stack[-1].description
        return ""
    
    def get_history(self, limit: int = 10) -> List[str]:
        """Get recent action history"""
        recent = self.undo_stack[-limit:]
        return [action.description for action in reversed(recent)]


class ElementUndoHelper:
    """
    Helper class for creating element-related undo actions
    """
    
    @staticmethod
    def create_move_action(element_id: str, old_pos: tuple, new_pos: tuple,
                          move_callback: Callable) -> UndoAction:
        """Create undo action for element move"""
        return UndoAction(
            action_type=ActionType.MOVE_ELEMENT,
            description=f"Move element",
            before_state=old_pos,
            after_state=new_pos,
            target_id=element_id,
            undo_func=lambda state: move_callback(element_id, state),
            redo_func=lambda state: move_callback(element_id, state)
        )
    
    @staticmethod
    def create_resize_action(element_id: str, old_size: tuple, new_size: tuple,
                           resize_callback: Callable) -> UndoAction:
        """Create undo action for element resize"""
        return UndoAction(
            action_type=ActionType.RESIZE_ELEMENT,
            description=f"Resize element",
            before_state=old_size,
            after_state=new_size,
            target_id=element_id,
            undo_func=lambda state: resize_callback(element_id, state),
            redo_func=lambda state: resize_callback(element_id, state)
        )
    
    @staticmethod
    def create_add_action(element_id: str, element_state: Any,
                         add_callback: Callable, remove_callback: Callable) -> UndoAction:
        """Create undo action for adding element"""
        return UndoAction(
            action_type=ActionType.ADD_ELEMENT,
            description=f"Add element",
            before_state=None,
            after_state=copy.deepcopy(element_state),
            target_id=element_id,
            undo_func=lambda state: remove_callback(element_id),
            redo_func=lambda state: add_callback(element_id, state)
        )
    
    @staticmethod
    def create_remove_action(element_id: str, element_state: Any,
                           add_callback: Callable, remove_callback: Callable) -> UndoAction:
        """Create undo action for removing element"""
        return UndoAction(
            action_type=ActionType.REMOVE_ELEMENT,
            description=f"Remove element",
            before_state=copy.deepcopy(element_state),
            after_state=None,
            target_id=element_id,
            undo_func=lambda state: add_callback(element_id, state),
            redo_func=lambda state: remove_callback(element_id)
        )
    
    @staticmethod
    def create_property_action(element_id: str, property_name: str,
                             old_value: Any, new_value: Any,
                             set_callback: Callable) -> UndoAction:
        """Create undo action for property change"""
        return UndoAction(
            action_type=ActionType.MODIFY_PROPERTY,
            description=f"Change {property_name}",
            before_state=old_value,
            after_state=new_value,
            target_id=element_id,
            undo_func=lambda state: set_callback(element_id, property_name, state),
            redo_func=lambda state: set_callback(element_id, property_name, state)
        )