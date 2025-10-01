"""
Visual effects: Glow, Blur, Color grading
"""
import cv2
import numpy as np
from typing import Tuple, Optional


class GlowEffect:
    """
    Gaussian blur-based glow effect
    """
    
    @staticmethod
    def apply(image: np.ndarray, blur_size: int = 31, 
              intensity: float = 0.5) -> np.ndarray:
        """
        Apply glow effect to image
        
        Args:
            image: Input image (BGR or RGB)
            blur_size: Kernel size for Gaussian blur (must be odd)
            intensity: Glow intensity (0.0 to 1.0)
            
        Returns:
            Image with glow effect applied
        """
        # Ensure blur_size is odd
        if blur_size % 2 == 0:
            blur_size += 1
        
        # Create blurred version
        blurred = cv2.GaussianBlur(image, (blur_size, blur_size), 0)
        
        # Blend original with blurred (additive)
        result = cv2.addWeighted(image, 1.0, blurred, intensity, 0)
        
        return result
    
    @staticmethod
    def apply_selective(image: np.ndarray, mask: np.ndarray, 
                       blur_size: int = 31, intensity: float = 0.5) -> np.ndarray:
        """
        Apply glow only to specific areas (defined by mask)
        
        Args:
            image: Input image
            mask: Binary mask (white = glow, black = no glow)
            blur_size: Kernel size
            intensity: Glow intensity
        """
        if blur_size % 2 == 0:
            blur_size += 1
        
        # Apply blur to entire image
        blurred = cv2.GaussianBlur(image, (blur_size, blur_size), 0)
        
        # Create glow layer
        glow = cv2.addWeighted(image, 0.5, blurred, intensity, 0)
        
        # Apply mask
        mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) if len(mask.shape) == 2 else mask
        mask_float = mask_3ch.astype(float) / 255.0
        
        result = (image * (1 - mask_float) + glow * mask_float).astype(np.uint8)
        
        return result


class NeonGlow:
    """
    Neon-style glow effect
    """
    
    @staticmethod
    def apply(image: np.ndarray, color: Tuple[int, int, int] = (0, 255, 255),
              blur_size: int = 51, intensity: float = 0.8) -> np.ndarray:
        """
        Apply neon glow effect
        
        Args:
            image: Input image
            color: Neon color (B, G, R)
            blur_size: Blur kernel size
            intensity: Effect intensity
        """
        if blur_size % 2 == 0:
            blur_size += 1
        
        # Convert to grayscale to find bright areas
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Threshold to find bright regions
        _, bright_mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        
        # Create colored glow layer
        glow_layer = np.zeros_like(image)
        glow_layer[:] = color
        
        # Apply mask to glow
        mask_3ch = cv2.cvtColor(bright_mask, cv2.COLOR_GRAY2BGR)
        glow_layer = cv2.bitwise_and(glow_layer, mask_3ch)
        
        # Blur the glow
        glow_blurred = cv2.GaussianBlur(glow_layer, (blur_size, blur_size), 0)
        
        # Blend with original
        result = cv2.addWeighted(image, 1.0, glow_blurred, intensity, 0)
        
        return result


class ChromaticAberration:
    """
    Chromatic aberration effect (RGB channel shift)
    """
    
    @staticmethod
    def apply(image: np.ndarray, shift: int = 5) -> np.ndarray:
        """
        Apply chromatic aberration
        
        Args:
            image: Input image (BGR)
            shift: Pixel shift amount
        """
        height, width = image.shape[:2]
        
        # Split channels
        b, g, r = cv2.split(image)
        
        # Shift red channel right
        M_r = np.float32([[1, 0, shift], [0, 1, 0]])
        r_shifted = cv2.warpAffine(r, M_r, (width, height))
        
        # Shift blue channel left
        M_b = np.float32([[1, 0, -shift], [0, 1, 0]])
        b_shifted = cv2.warpAffine(b, M_b, (width, height))
        
        # Merge back
        result = cv2.merge([b_shifted, g, r_shifted])
        
        return result


class VignetteEffect:
    """
    Vignette effect (darkened edges)
    """
    
    @staticmethod
    def apply(image: np.ndarray, strength: float = 0.5) -> np.ndarray:
        """
        Apply vignette effect
        
        Args:
            image: Input image
            strength: Vignette strength (0.0 to 1.0)
        """
        height, width = image.shape[:2]
        
        # Create radial gradient mask
        X, Y = np.meshgrid(np.linspace(-1, 1, width), np.linspace(-1, 1, height))
        radius = np.sqrt(X**2 + Y**2)
        
        # Normalize and invert
        vignette = 1 - np.clip(radius * strength, 0, 1)
        
        # Apply to each channel
        vignette_3ch = np.stack([vignette] * 3, axis=2)
        result = (image * vignette_3ch).astype(np.uint8)
        
        return result


class MotionBlur:
    """
    Directional motion blur effect
    """
    
    @staticmethod
    def apply(image: np.ndarray, size: int = 15, angle: float = 0) -> np.ndarray:
        """
        Apply motion blur
        
        Args:
            image: Input image
            size: Blur length
            angle: Blur direction in degrees (0 = horizontal)
        """
        # Create motion blur kernel
        kernel = np.zeros((size, size))
        kernel[int((size - 1) / 2), :] = np.ones(size)
        kernel = kernel / size
        
        # Rotate kernel
        M = cv2.getRotationMatrix2D((size / 2, size / 2), angle, 1.0)
        kernel = cv2.warpAffine(kernel, M, (size, size))
        
        # Apply blur
        result = cv2.filter2D(image, -1, kernel)
        
        return result


class ParticleEffect:
    """
    Particle overlay effect
    """
    
    def __init__(self, width: int, height: int, num_particles: int = 100):
        self.width = width
        self.height = height
        self.num_particles = num_particles
        
        # Initialize particles
        self.particles = []
        for _ in range(num_particles):
            self.particles.append({
                'x': np.random.randint(0, width),
                'y': np.random.randint(0, height),
                'vx': np.random.uniform(-2, 2),
                'vy': np.random.uniform(-2, 2),
                'size': np.random.randint(1, 4),
                'alpha': np.random.uniform(0.3, 1.0)
            })
    
    def update(self):
        """Update particle positions"""
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            
            # Wrap around edges
            if p['x'] < 0:
                p['x'] = self.width
            elif p['x'] > self.width:
                p['x'] = 0
            
            if p['y'] < 0:
                p['y'] = self.height
            elif p['y'] > self.height:
                p['y'] = 0
    
    def render(self, image: np.ndarray, color: Tuple[int, int, int] = (255, 255, 255)) -> np.ndarray:
        """Render particles on image"""
        result = image.copy()
        
        for p in self.particles:
            # Draw particle as circle
            cv2.circle(
                result,
                (int(p['x']), int(p['y'])),
                p['size'],
                color,
                -1
            )
        
        return result


class ColorGrading:
    """
    Color grading and LUT effects
    """
    
    @staticmethod
    def warm(image: np.ndarray, intensity: float = 0.3) -> np.ndarray:
        """Apply warm color grade"""
        # Increase red/yellow, decrease blue
        result = image.copy().astype(float)
        result[:, :, 2] *= (1 + intensity)  # Red
        result[:, :, 1] *= (1 + intensity * 0.5)  # Green
        result[:, :, 0] *= (1 - intensity * 0.3)  # Blue
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    @staticmethod
    def cool(image: np.ndarray, intensity: float = 0.3) -> np.ndarray:
        """Apply cool color grade"""
        result = image.copy().astype(float)
        result[:, :, 0] *= (1 + intensity)  # Blue
        result[:, :, 1] *= (1 + intensity * 0.3)  # Green
        result[:, :, 2] *= (1 - intensity * 0.3)  # Red
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    @staticmethod
    def vintage(image: np.ndarray) -> np.ndarray:
        """Apply vintage film look"""
        # Sepia tone
        kernel = np.array([[0.272, 0.534, 0.131],
                          [0.349, 0.686, 0.168],
                          [0.393, 0.769, 0.189]])
        
        result = cv2.transform(image, kernel)
        
        # Reduce contrast slightly
        result = cv2.addWeighted(result, 0.9, result, 0, 10)
        
        # Add slight vignette
        result = VignetteEffect.apply(result, 0.3)
        
        return result
