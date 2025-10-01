"""
Video background support
"""
import cv2
import numpy as np
from typing import Optional


class VideoBackground:
    """
    Handles video file as animated background
    """
    
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.cap: Optional[cv2.VideoCapture] = None
        self.fps = 30
        self.total_frames = 0
        self.duration = 0.0
        self.width = 1920
        self.height = 1080
        self.loop = True
        
        self.current_frame_index = 0
        self.frame_cache = {}
        self.cache_size = 100  # Cache last 100 frames
        
        self.load_video()
    
    def load_video(self) -> bool:
        """Load video file"""
        try:
            self.cap = cv2.VideoCapture(self.video_path)
            
            if not self.cap.isOpened():
                return False
            
            # Get video properties
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.duration = self.total_frames / self.fps
            
            return True
            
        except Exception as e:
            print(f"Error loading video background: {e}")
            return False
    
    def get_frame(self, time_pos: float, target_size: tuple = None) -> Optional[np.ndarray]:
        """
        Get frame at specific time position
        
        Args:
            time_pos: Time position in seconds
            target_size: (width, height) to resize to
            
        Returns:
            Frame as numpy array (BGR format)
        """
        if not self.cap or not self.cap.isOpened():
            return None
        
        # Handle looping
        if self.loop:
            time_pos = time_pos % self.duration
        elif time_pos >= self.duration:
            time_pos = self.duration - 0.001
        
        # Calculate frame index
        frame_index = int(time_pos * self.fps)
        frame_index = min(frame_index, self.total_frames - 1)
        
        # Check cache
        if frame_index in self.frame_cache:
            frame = self.frame_cache[frame_index]
        else:
            # Seek to frame
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame = self.cap.read()
            
            if not ret:
                return None
            
            # Cache frame
            self.frame_cache[frame_index] = frame.copy()
            
            # Limit cache size
            if len(self.frame_cache) > self.cache_size:
                # Remove oldest frame
                oldest = min(self.frame_cache.keys())
                del self.frame_cache[oldest]
        
        # Resize if requested
        if target_size and (frame.shape[1] != target_size[0] or frame.shape[0] != target_size[1]):
            frame = cv2.resize(frame, target_size, interpolation=cv2.INTER_LINEAR)
        
        return frame
    
    def release(self):
        """Release video capture"""
        if self.cap:
            self.cap.release()
            self.cap = None
        
        self.frame_cache.clear()
    
    def __del__(self):
        """Cleanup on delete"""
        self.release()


class VideoBlender:
    """
    Utilities for blending video backgrounds with content
    """
    
    @staticmethod
    def blend_overlay(background: np.ndarray, overlay: np.ndarray, 
                     alpha: float = 0.7) -> np.ndarray:
        """
        Blend overlay on background
        
        Args:
            background: Background frame
            overlay: Overlay frame (content)
            alpha: Overlay opacity (0-1)
            
        Returns:
            Blended frame
        """
        return cv2.addWeighted(background, 1 - alpha, overlay, alpha, 0)
    
    @staticmethod
    def blend_screen(background: np.ndarray, overlay: np.ndarray) -> np.ndarray:
        """Screen blend mode (lighter)"""
        bg_float = background.astype(float) / 255
        ov_float = overlay.astype(float) / 255
        
        result = 1 - (1 - bg_float) * (1 - ov_float)
        return (result * 255).astype(np.uint8)
    
    @staticmethod
    def blend_multiply(background: np.ndarray, overlay: np.ndarray) -> np.ndarray:
        """Multiply blend mode (darker)"""
        bg_float = background.astype(float) / 255
        ov_float = overlay.astype(float) / 255
        
        result = bg_float * ov_float
        return (result * 255).astype(np.uint8)
    
    @staticmethod
    def apply_blur_background(video_frame: np.ndarray, blur_amount: int = 25) -> np.ndarray:
        """Apply blur to video background for better overlay visibility"""
        if blur_amount % 2 == 0:
            blur_amount += 1
        
        return cv2.GaussianBlur(video_frame, (blur_amount, blur_amount), 0)
    
    @staticmethod
    def darken_background(video_frame: np.ndarray, amount: float = 0.5) -> np.ndarray:
        """Darken video background"""
        return (video_frame * amount).astype(np.uint8)
