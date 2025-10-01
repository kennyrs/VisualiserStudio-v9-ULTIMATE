"""
Video export engine using FFmpeg
"""
import cv2
import numpy as np
import subprocess
import os
from typing import List, Optional
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QPainter, QImage
from PyQt6.QtWidgets import QGraphicsScene

from models.project_state import ProjectState
from models.audio_processor import AudioProcessor
from elements.base_element import DraggableElement


class VideoExporter(QThread):
    """
    Background thread for video export
    Renders frames and encodes to video
    """
    
    progress = pyqtSignal(int)  # 0-100
    status = pyqtSignal(str)  # Status message
    finished = pyqtSignal(str)  # Output path
    error = pyqtSignal(str)  # Error message
    
    def __init__(self, project: ProjectState, audio_processor: AudioProcessor,
                 elements: List[DraggableElement], output_path: str,
                 background_image: Optional[np.ndarray] = None):
        super().__init__()
        self.project = project
        self.audio_processor = audio_processor
        self.elements = elements
        self.output_path = output_path
        self.background_image = background_image
        
        self.is_cancelled = False
    
    def run(self):
        """Main export process"""
        try:
            self.status.emit("Initializing export...")
            
            # Calculate total frames
            duration = self.audio_processor.duration
            fps = self.project.fps
            total_frames = int(duration * fps)
            
            if total_frames == 0:
                self.error.emit("Invalid duration or FPS")
                return
            
            # Create temporary video file (without audio)
            temp_video = self.output_path.replace('.mp4', '_temp.mp4')
            
            self.status.emit("Rendering frames...")
            success = self.render_frames(temp_video, total_frames, fps)
            
            if not success or self.is_cancelled:
                self.cleanup_temp_files(temp_video)
                return
            
            # Combine video with audio using FFmpeg
            self.status.emit("Encoding final video...")
            success = self.combine_audio_video(temp_video)
            
            if not success:
                self.error.emit("Failed to combine audio and video")
                self.cleanup_temp_files(temp_video)
                return
            
            # Cleanup
            self.cleanup_temp_files(temp_video)
            
            self.status.emit("Export complete!")
            self.finished.emit(self.output_path)
            
        except Exception as e:
            self.error.emit(f"Export failed: {str(e)}")
    
    def render_frames(self, temp_video: str, total_frames: int, fps: int) -> bool:
        """Render all frames to temporary video"""
        try:
            width, height = self.project.resolution
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))
            
            if not writer.isOpened():
                self.error.emit("Failed to create video writer")
                return False
            
            # Render each frame
            for frame_idx in range(total_frames):
                if self.is_cancelled:
                    writer.release()
                    return False
                
                # Calculate time position
                time_pos = frame_idx / fps
                
                # Render frame
                frame = self.render_frame(time_pos, width, height)
                
                # Write frame
                writer.write(frame)
                
                # Update progress
                progress = int((frame_idx / total_frames) * 90)  # 0-90%
                self.progress.emit(progress)
                
                # Status update every second
                if frame_idx % fps == 0:
                    seconds = int(time_pos)
                    total_seconds = int(self.audio_processor.duration)
                    self.status.emit(f"Rendering: {seconds}/{total_seconds}s")
            
            writer.release()
            return True
            
        except Exception as e:
            self.error.emit(f"Frame rendering failed: {str(e)}")
            return False
    
    def render_frame(self, time_pos: float, width: int, height: int) -> np.ndarray:
        """Render a single frame at given time position"""
        # Create base frame
        if self.background_image is not None:
            frame = self.background_image.copy()
        else:
            # Black background
            frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Create QImage for rendering with Qt
        qimage = QImage(frame.data, width, height, width * 3, QImage.Format.Format_RGB888)
        
        # Create painter
        painter = QPainter(qimage)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Update and render each element
        from elements.visualizer_element import VisualizerElement
        
        for element in sorted(self.elements, key=lambda e: e.state.z_index):
            if not element.state.visible:
                continue
            
            # Update visualizer spectrum
            if isinstance(element, VisualizerElement):
                element.update_spectrum(time_pos)
            
            # Save painter state
            painter.save()
            
            # Translate to element position
            painter.translate(element.state.x, element.state.y)
            
            # Render element
            element.paint(painter, None, None)
            
            # Restore painter state
            painter.restore()
        
        painter.end()
        
        # Convert QImage back to numpy array
        ptr = qimage.bits()
        ptr.setsize(height * width * 3)
        arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 3))
        
        # Convert RGB to BGR for OpenCV
        frame = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        
        return frame
    
    def combine_audio_video(self, temp_video: str) -> bool:
        """Combine temporary video with audio using FFmpeg"""
        try:
            # FFmpeg command
            cmd = [
                'ffmpeg',
                '-y',  # Overwrite output
                '-i', temp_video,  # Video input
                '-i', self.project.audio_path,  # Audio input
                '-c:v', 'libx264',  # Video codec
                '-preset', 'medium',  # Encoding preset
                '-crf', str(self.project.crf),  # Quality
                '-c:a', 'aac',  # Audio codec
                '-b:a', '320k',  # Audio bitrate
                '-shortest',  # End at shortest stream
                self.output_path
            ]
            
            # Run FFmpeg
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Wait for completion
            stdout, stderr = process.communicate()
            
            # Update progress
            self.progress.emit(100)
            
            if process.returncode != 0:
                self.error.emit(f"FFmpeg error: {stderr}")
                return False
            
            return True
            
        except FileNotFoundError:
            self.error.emit("FFmpeg not found. Please install FFmpeg.")
            return False
        except Exception as e:
            self.error.emit(f"Audio/Video combination failed: {str(e)}")
            return False
    
    def cleanup_temp_files(self, temp_video: str):
        """Clean up temporary files"""
        try:
            if os.path.exists(temp_video):
                os.remove(temp_video)
        except:
            pass
    
    def cancel(self):
        """Cancel export"""
        self.is_cancelled = True
