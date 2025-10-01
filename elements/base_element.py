"""
Base draggable and resizable element
"""
from enum import Enum
from PyQt6.QtWidgets import QGraphicsItem, QGraphicsRectItem
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPen, QBrush, QColor, QPainter
from typing import Optional

from models.project_state import ElementState
from utils.config import RESIZE_HANDLE_SIZE, MIN_ELEMENT_SIZE


class ResizeHandle(Enum):
    """Resize handle positions"""
    NONE = 0
    TOP_LEFT = 1
    TOP = 2
    TOP_RIGHT = 3
    RIGHT = 4
    BOTTOM_RIGHT = 5
    BOTTOM = 6
    BOTTOM_LEFT = 7
    LEFT = 8


class DraggableElement(QGraphicsItem):
    """
    Base class for all draggable and resizable elements
    
    Features:
    - Drag and drop positioning
    - 8-point resize handles
    - Lock/unlock functionality
    - Visual selection indicator
    """
    
    def __init__(self, state: ElementState):
        super().__init__()
        self.state = state
        
        # Make item interactive
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        
        # Resize state
        self.resize_mode: ResizeHandle = ResizeHandle.NONE
        self.resize_start_pos = QPointF()
        self.resize_start_rect = QRectF()
        
        # Visual properties
        self.selection_pen = QPen(QColor(0, 255, 255), 2, Qt.PenStyle.DashLine)
        self.handle_brush = QBrush(QColor(255, 255, 255))
        self.handle_pen = QPen(QColor(0, 0, 0), 1)
        
    def boundingRect(self) -> QRectF:
        """Define the bounding rectangle"""
        return QRectF(0, 0, self.state.width, self.state.height)
    
    def paint(self, painter: QPainter, option, widget):
        """
        Paint the element - override in subclasses
        This base implementation draws selection border and handles
        """
        if self.isSelected() and not self.state.locked:
            # Draw selection border
            painter.setPen(self.selection_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(self.boundingRect())
            
            # Draw resize handles
            self._draw_resize_handles(painter)
    
    def _draw_resize_handles(self, painter: QPainter):
        """Draw 8 resize handles"""
        painter.setBrush(self.handle_brush)
        painter.setPen(self.handle_pen)
        
        w = self.state.width
        h = self.state.height
        s = RESIZE_HANDLE_SIZE
        
        # 8 handle positions
        handles = [
            (0, 0),              # TOP_LEFT
            (w/2 - s/2, 0),      # TOP
            (w - s, 0),          # TOP_RIGHT
            (w - s, h/2 - s/2),  # RIGHT
            (w - s, h - s),      # BOTTOM_RIGHT
            (w/2 - s/2, h - s),  # BOTTOM
            (0, h - s),          # BOTTOM_LEFT
            (0, h/2 - s/2),      # LEFT
        ]
        
        for x, y in handles:
            painter.drawRect(QRectF(x, y, s, s))
    
    def mousePressEvent(self, event):
        """Handle mouse press - detect resize or drag"""
        if self.state.locked:
            event.ignore()
            return
        
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.pos()
            self.resize_mode = self._get_resize_handle(pos)
            
            if self.resize_mode != ResizeHandle.NONE:
                # Start resize
                self.resize_start_pos = event.scenePos()
                self.resize_start_rect = QRectF(
                    self.state.x, self.state.y,
                    self.state.width, self.state.height
                )
                self._update_cursor(self.resize_mode)
                event.accept()
            else:
                # Start drag
                super().mousePressEvent(event)
        else:
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Handle mouse move - resize or drag"""
        if self.resize_mode != ResizeHandle.NONE:
            # Resize operation
            delta = event.scenePos() - self.resize_start_pos
            self._handle_resize(delta)
            event.accept()
        else:
            # Drag operation
            super().mouseMoveEvent(event)
            # Update state position
            self.state.x = self.pos().x()
            self.state.y = self.pos().y()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release - end resize or drag"""
        if self.resize_mode != ResizeHandle.NONE:
            self.resize_mode = ResizeHandle.NONE
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)
    
    def _get_resize_handle(self, pos: QPointF) -> ResizeHandle:
        """Detect which resize handle was clicked"""
        w = self.state.width
        h = self.state.height
        s = RESIZE_HANDLE_SIZE
        
        # Check each handle
        handles = [
            (ResizeHandle.TOP_LEFT, QRectF(0, 0, s, s)),
            (ResizeHandle.TOP, QRectF(w/2 - s/2, 0, s, s)),
            (ResizeHandle.TOP_RIGHT, QRectF(w - s, 0, s, s)),
            (ResizeHandle.RIGHT, QRectF(w - s, h/2 - s/2, s, s)),
            (ResizeHandle.BOTTOM_RIGHT, QRectF(w - s, h - s, s, s)),
            (ResizeHandle.BOTTOM, QRectF(w/2 - s/2, h - s, s, s)),
            (ResizeHandle.BOTTOM_LEFT, QRectF(0, h - s, s, s)),
            (ResizeHandle.LEFT, QRectF(0, h/2 - s/2, s, s)),
        ]
        
        for handle, rect in handles:
            if rect.contains(pos):
                return handle
        
        return ResizeHandle.NONE
    
    def _handle_resize(self, delta: QPointF):
        """Handle resize operation based on active handle"""
        rect = self.resize_start_rect
        
        if self.resize_mode == ResizeHandle.TOP_LEFT:
            new_x = rect.x() + delta.x()
            new_y = rect.y() + delta.y()
            new_w = rect.width() - delta.x()
            new_h = rect.height() - delta.y()
        elif self.resize_mode == ResizeHandle.TOP:
            new_x = rect.x()
            new_y = rect.y() + delta.y()
            new_w = rect.width()
            new_h = rect.height() - delta.y()
        elif self.resize_mode == ResizeHandle.TOP_RIGHT:
            new_x = rect.x()
            new_y = rect.y() + delta.y()
            new_w = rect.width() + delta.x()
            new_h = rect.height() - delta.y()
        elif self.resize_mode == ResizeHandle.RIGHT:
            new_x = rect.x()
            new_y = rect.y()
            new_w = rect.width() + delta.x()
            new_h = rect.height()
        elif self.resize_mode == ResizeHandle.BOTTOM_RIGHT:
            new_x = rect.x()
            new_y = rect.y()
            new_w = rect.width() + delta.x()
            new_h = rect.height() + delta.y()
        elif self.resize_mode == ResizeHandle.BOTTOM:
            new_x = rect.x()
            new_y = rect.y()
            new_w = rect.width()
            new_h = rect.height() + delta.y()
        elif self.resize_mode == ResizeHandle.BOTTOM_LEFT:
            new_x = rect.x() + delta.x()
            new_y = rect.y()
            new_w = rect.width() - delta.x()
            new_h = rect.height() + delta.y()
        elif self.resize_mode == ResizeHandle.LEFT:
            new_x = rect.x() + delta.x()
            new_y = rect.y()
            new_w = rect.width() - delta.x()
            new_h = rect.height()
        else:
            return
        
        # Apply minimum size constraint
        if new_w >= MIN_ELEMENT_SIZE and new_h >= MIN_ELEMENT_SIZE:
            self.prepareGeometryChange()
            self.state.x = new_x
            self.state.y = new_y
            self.state.width = new_w
            self.state.height = new_h
            self.setPos(new_x, new_y)
            self.update()
    
    def _update_cursor(self, handle: ResizeHandle):
        """Update cursor based on resize handle"""
        cursors = {
            ResizeHandle.TOP_LEFT: Qt.CursorShape.SizeFDiagCursor,
            ResizeHandle.TOP: Qt.CursorShape.SizeVerCursor,
            ResizeHandle.TOP_RIGHT: Qt.CursorShape.SizeBDiagCursor,
            ResizeHandle.RIGHT: Qt.CursorShape.SizeHorCursor,
            ResizeHandle.BOTTOM_RIGHT: Qt.CursorShape.SizeFDiagCursor,
            ResizeHandle.BOTTOM: Qt.CursorShape.SizeVerCursor,
            ResizeHandle.BOTTOM_LEFT: Qt.CursorShape.SizeBDiagCursor,
            ResizeHandle.LEFT: Qt.CursorShape.SizeHorCursor,
        }
        
        cursor = cursors.get(handle, Qt.CursorShape.ArrowCursor)
        self.setCursor(cursor)
