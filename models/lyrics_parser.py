"""
LRC Lyrics parser with synchronization
"""
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class LyricLine:
    """Single lyric line with timestamp"""
    timestamp: float  # Time in seconds
    text: str
    
    def __repr__(self):
        mins = int(self.timestamp // 60)
        secs = self.timestamp % 60
        return f"[{mins:02d}:{secs:05.2f}] {self.text}"


class LyricsParser:
    """
    Parse and manage LRC format lyrics
    
    LRC Format:
    [00:12.50]First line of lyrics
    [00:17.30]Second line
    [ti:Song Title]
    [ar:Artist]
    """
    
    def __init__(self):
        self.lines: List[LyricLine] = []
        self.metadata = {}
        self.current_index = 0
    
    def load_from_file(self, filepath: str) -> bool:
        """Load lyrics from LRC file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self.parse(content)
        except Exception as e:
            print(f"Error loading lyrics: {e}")
            return False
    
    def parse(self, content: str) -> bool:
        """Parse LRC content"""
        self.lines.clear()
        self.metadata.clear()
        
        # Regex patterns
        timestamp_pattern = re.compile(r'\[(\d+):(\d+)\.(\d+)\](.+)')
        metadata_pattern = re.compile(r'\[([a-z]+):(.+)\]')
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Try metadata
            meta_match = metadata_pattern.match(line)
            if meta_match and len(meta_match.group(1)) == 2:
                key = meta_match.group(1)
                value = meta_match.group(2).strip()
                self.metadata[key] = value
                continue
            
            # Try timestamp
            time_match = timestamp_pattern.match(line)
            if time_match:
                minutes = int(time_match.group(1))
                seconds = int(time_match.group(2))
                centiseconds = int(time_match.group(3))
                text = time_match.group(4).strip()
                
                # Convert to total seconds
                timestamp = minutes * 60 + seconds + centiseconds / 100.0
                
                self.lines.append(LyricLine(timestamp, text))
        
        # Sort by timestamp
        self.lines.sort(key=lambda x: x.timestamp)
        
        return len(self.lines) > 0
    
    def get_current_lyric(self, time_pos: float) -> Optional[str]:
        """Get lyric line for current time position"""
        if not self.lines:
            return None
        
        # Find appropriate line
        for i, line in enumerate(self.lines):
            if line.timestamp > time_pos:
                # Return previous line
                if i > 0:
                    return self.lines[i - 1].text
                return None
        
        # Return last line if past all timestamps
        return self.lines[-1].text if self.lines else None
    
    def get_upcoming_lyric(self, time_pos: float, lookahead: float = 2.0) -> Optional[str]:
        """Get upcoming lyric within lookahead seconds"""
        if not self.lines:
            return None
        
        for line in self.lines:
            if time_pos < line.timestamp <= time_pos + lookahead:
                return line.text
        
        return None
    
    def get_lyric_window(self, time_pos: float, before: int = 1, after: int = 2) -> List[Tuple[str, bool]]:
        """
        Get window of lyrics around current time
        Returns list of (text, is_current) tuples
        """
        if not self.lines:
            return []
        
        # Find current line index
        current_idx = -1
        for i, line in enumerate(self.lines):
            if line.timestamp <= time_pos:
                current_idx = i
            else:
                break
        
        if current_idx < 0:
            # Before first line
            start_idx = 0
            end_idx = min(after + 1, len(self.lines))
            current_idx = -1
        else:
            start_idx = max(0, current_idx - before)
            end_idx = min(len(self.lines), current_idx + after + 1)
        
        result = []
        for i in range(start_idx, end_idx):
            result.append((self.lines[i].text, i == current_idx))
        
        return result
    
    def get_metadata(self, key: str, default: str = "") -> str:
        """Get metadata value"""
        return self.metadata.get(key, default)
    
    def create_sample_lrc(self, output_path: str):
        """Create sample LRC file"""
        sample = """[ti:Sample Song]
[ar:Sample Artist]
[al:Sample Album]
[by:VisualiserStudio]

[00:12.50]First line of the song
[00:17.30]Second line appears here
[00:23.00]Third line follows
[00:28.50]And so on through the track
[00:34.00]Lyrics synchronized to music
[00:39.50]Creating perfect timing
[00:45.00]For your visual experience
"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(sample)


class KaraokeStyler:
    """Helper for karaoke-style highlighting"""
    
    @staticmethod
    def get_progress_color(base_color: Tuple[int, int, int], 
                          highlight_color: Tuple[int, int, int],
                          progress: float) -> Tuple[int, int, int]:
        """
        Interpolate between base and highlight color
        progress: 0.0 to 1.0
        """
        r = int(base_color[0] + (highlight_color[0] - base_color[0]) * progress)
        g = int(base_color[1] + (highlight_color[1] - base_color[1]) * progress)
        b = int(base_color[2] + (highlight_color[2] - base_color[2]) * progress)
        return (r, g, b)
