"""
Audio processing and FFT analysis
"""
import numpy as np
import librosa
import soundfile as sf
from typing import Optional, Tuple
import pygame


class AudioProcessor:
    """
    Handles audio loading, FFT analysis, and playback
    """
    
    def __init__(self):
        self.audio: Optional[np.ndarray] = None
        self.sample_rate: int = 22050
        self.duration: float = 0.0
        self.filepath: Optional[str] = None
        
        # Pygame mixer for playback
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.is_playing = False
        self.playback_start_time = 0.0
        
        # Cache for spectrum data
        self._spectrum_cache = {}
        
    def load_audio(self, filepath: str) -> bool:
        """
        Load audio file and prepare for processing
        
        Args:
            filepath: Path to audio file (MP3, WAV, etc)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load audio with librosa
            self.audio, self.sample_rate = librosa.load(filepath, sr=22050, mono=True)
            self.duration = len(self.audio) / self.sample_rate
            self.filepath = filepath
            
            # Load for pygame playback
            pygame.mixer.music.load(filepath)
            
            # Clear cache
            self._spectrum_cache.clear()
            
            return True
            
        except Exception as e:
            print(f"Error loading audio: {e}")
            return False
    
    def get_spectrum(self, time_pos: float, num_bands: int = 20) -> np.ndarray:
        """
        Get frequency spectrum at specific time position
        
        Args:
            time_pos: Time position in seconds
            num_bands: Number of frequency bands to return
            
        Returns:
            Array of normalized levels (0-1) for each frequency band
        """
        if self.audio is None:
            return np.zeros(num_bands)
        
        # Check cache
        cache_key = (int(time_pos * 100), num_bands)
        if cache_key in self._spectrum_cache:
            return self._spectrum_cache[cache_key]
        
        # Get audio window
        sample_idx = int(time_pos * self.sample_rate)
        window_size = 2048
        
        # Extract window with bounds checking
        start = max(0, sample_idx - window_size // 2)
        end = min(len(self.audio), sample_idx + window_size // 2)
        window = self.audio[start:end]
        
        # Pad if necessary
        if len(window) < window_size:
            window = np.pad(window, (0, window_size - len(window)))
        
        # Apply Hanning window to reduce spectral leakage
        window = window * np.hanning(len(window))
        
        # FFT
        spectrum = np.fft.rfft(window)
        magnitude = np.abs(spectrum)
        
        # Group into frequency bands (logarithmic scale)
        bands = np.zeros(num_bands)
        for i in range(num_bands):
            # Logarithmic frequency distribution
            start_idx = int((i / num_bands) ** 2 * len(magnitude))
            end_idx = int(((i + 1) / num_bands) ** 2 * len(magnitude))
            
            if end_idx > start_idx:
                bands[i] = np.mean(magnitude[start_idx:end_idx])
        
        # Normalize to 0-1 range
        max_val = np.max(bands)
        if max_val > 0:
            bands = bands / max_val
        
        # Apply some scaling for better visual results
        bands = np.clip(bands * 1.5, 0, 1)
        
        # Cache result
        self._spectrum_cache[cache_key] = bands
        
        return bands
    
    def play(self, start_time: float = 0.0):
        """Start audio playback from specified time"""
        if self.filepath is None:
            return
        
        pygame.mixer.music.play(start=start_time)
        self.is_playing = True
        self.playback_start_time = start_time
    
    def pause(self):
        """Pause audio playback"""
        pygame.mixer.music.pause()
        self.is_playing = False
    
    def resume(self):
        """Resume audio playback"""
        pygame.mixer.music.unpause()
        self.is_playing = True
    
    def stop(self):
        """Stop audio playback"""
        pygame.mixer.music.stop()
        self.is_playing = False
    
    def get_playback_position(self) -> float:
        """Get current playback position in seconds"""
        if not self.is_playing:
            return self.playback_start_time
        
        # pygame.mixer.music.get_pos() returns milliseconds
        pos_ms = pygame.mixer.music.get_pos()
        return self.playback_start_time + (pos_ms / 1000.0)
    
    def seek(self, time_pos: float):
        """Seek to specific time position"""
        was_playing = self.is_playing
        self.stop()
        
        if was_playing:
            self.play(start_time=time_pos)
        else:
            self.playback_start_time = time_pos
