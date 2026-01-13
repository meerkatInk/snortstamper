import ollama
import re
from typing import List, Dict, Tuple
import json

class ChapterGenerator:
    def __init__(self, model="mistral", chunk_size=4000, overlap=800):
        """
        Initialize the chapter generator.
        
        Args:
            model: Ollama model name
            chunk_size: Number of characters per chunk
            overlap: Number of characters to overlap between chunks for context
        """
        self.model = model
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.previous_chapters = []
        self.context_summary = ""
        
    def parse_timestamp(self, timestamp_str: str) -> int:
        """Convert timestamp string to seconds."""
        timestamp_str = timestamp_str.strip('[]').strip()
        parts = timestamp_str.split(':')
        
        if len(parts) == 2:  # MM:SS or M:SS
            minutes, seconds = parts
            return int(minutes) * 60 + int(seconds)
        elif len(parts) == 3:  # H:MM:SS
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        return 0
    
    def format_timestamp(self, seconds: int) -> str:
        """Convert seconds back to timestamp format."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"
    
    def extract_timestamp_from_line(self, line: str) -> Tuple[str, str]:
        """
        Extract timestamp and text from a line.
        Returns (timestamp, text) or (None, line) if no timestamp found.
        """
        match = re.match(r'^\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*(.*)$', line)
        if match:
            return match.group(1), match.group(2)
        return None, line
    
    def chunk_transcript(self, transcript: str) -> List[Dict]:
        """
        Split transcript into overlapping chunks with timestamps.
        
        Args:
            transcript: Full transcript with [timestamp] format
            
        Returns:
            List of chunks with metadata
        """
        lines = transcript.strip().split('\n')
        chunks = []
        current_chunk_lines = []
        current_length = 0
        chunk_start_timestamp = None
        chunk_start_seconds = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            timestamp, text = self.extract_timestamp_from_line(line)
            
            # Track the first timestamp of this chunk
            if timestamp and chunk_start_timestamp is None:
                chunk_start_timestamp = timestamp
                chunk_start_seconds = self.parse_timestamp(timestamp)
            
            line_length = len(line)
            
            # Check if we should start a new chunk
            if current_length + line_length > self.chunk_size and current_chunk_lines:
                # Save current chunk
                chunks.append({
                    'text': '\n'.join(current_chunk_lines),
                    'start_timestamp': chunk_start_timestamp,
                    'start_seconds': chunk_start_seconds
                })
                
                # Calculate overlap: keep last ~overlap characters
                overlap_text = '\n'.join(current_chunk_lines)
                if len(overlap_text) > self.overlap:
                    # Keep roughly the last 1/4 of lines for context
                    keep_lines = max(3, len(current_chunk_lines) // 4)
                    current_chunk_lines = current_chunk_lines[-keep_lines:]
                    current_length = sum(len(l) for l in current_chunk_lines)
                else:
                    current_chunk_lines = []
                    current_length = 0
                
                chunk_start_timestamp = None
                chunk_start_seconds = None
            
            current_chunk_lines.append(line)
            current_length += line_length
        
        # Add final chunk
        if current_chunk_lines:
            chunks.append({
                'text': '\n'.join(current_chunk_lines),
                'start_timestamp': chunk_start_timestamp,
                'start_seconds': chunk_start_seconds
            })
        
        return chunks
    
    def generate_context_summary(self, chunk_text: str) -> str:
        """Generate a brief summary of the chunk for context in next iteration."""
        prompt = f"""Summarize the main topics covered in this transcript segment in 2-3 sentences. Focus on what was discussed, not how it was presented.

Transcript:
{chunk_text[:1500]}

Brief summary:"""
        
        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={'temperature': 0.3, 'num_predict': 100}
            )
            return response['response'].strip()
        except Exception as e:
            print(f"Warning: Could not generate summary: {e}")
            return ""
    
    def generate_chapters_for_chunk(self, chunk: Dict, chunk_index: int, total_chunks: int) -> List[Dict]:
        """Generate chapters for a single chunk with full context."""
        
        # Build context prompt
        context_info = ""
        if self.previous_chapters:
            recent_chapters = self.previous_chapters[-3:]
            context_info = "Previously identified chapters:\n"
            for ch in recent_chapters:
                context_info += f"- {ch['timestamp']} {ch['title']}\n"
            context_info += "\n"
        
        if self.context_summary:
            context_info += f"What was covered before: {self.context_summary}\n\n"
        
        chunk_position = f"[Processing segment {chunk_index + 1} of {total_chunks}]"
        
        prompt = f"""{chunk_position}

{context_info}Analyze this YouTube video transcript segment and identify major chapter points.

RULES:
1. Only create chapters for CLEAR topic changes or new segments
2. Use EXACT timestamps from the transcript in [M:SS] or [H:MM:SS] format
3. Create engaging, specific chapter titles (5-12 words)
4. Aim for 1 chapter every 3-7 minutes (don't over-segment)
5. Build on previous chapters - avoid repeating similar topics
6. If this chunk has no major topic changes, output "NO_CHAPTERS"

Transcript:
{chunk['text']}

Output format (one per line):
[M:SS] Chapter Title Here
or
[H:MM:SS] Chapter Title Here

Chapters:"""
        
        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': 0.25,
                    'top_p': 0.9,
                    'num_predict': 200
                }
            )
            
            # Parse response
            chapters = []
            response_text = response['response'].strip()
            
            if "NO_CHAPTERS" in response_text.upper():
                return chapters
            
            lines = response_text.split('\n')
            
            for line in lines:
                # Match [timestamp] - title or [timestamp] title format
                match = re.match(r'\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*[-–—]?\s*(.+)', line.strip())
                if match:
                    timestamp, title = match.groups()
                    title = title.strip()
                    
                    # Clean up title
                    title = re.sub(r'^[-–—]\s*', '', title)
                    
                    if len(title) > 10:  # Ensure substantial title
                        chapters.append({
                            'timestamp': timestamp,
                            'title': title,
                            'timestamp_seconds': self.parse_timestamp(timestamp)
                        })
            
            return chapters
            
        except Exception as e:
            print(f"Error generating chapters for chunk {chunk_index + 1}: {e}")
            return []
    
    def deduplicate_chapters(self, chapters: List[Dict]) -> List[Dict]:
        """Remove duplicate or very similar chapters."""
        if not chapters:
            return []
        
        unique_chapters = [chapters[0]]
        
        for chapter in chapters[1:]:
            time_diff = abs(chapter['timestamp_seconds'] - unique_chapters[-1]['timestamp_seconds'])
            
            # Skip if too close to previous chapter (within 45 seconds)
            if time_diff < 45:
                # Keep the one with longer/better title
                if len(chapter['title']) > len(unique_chapters[-1]['title']):
                    unique_chapters[-1] = chapter
            else:
                unique_chapters.append(chapter)
        
        return unique_chapters
    
    def generate_chapters(self, transcript: str) -> List[Dict]:
        """
        Generate YouTube chapters from full transcript.
        
        Args:
            transcript: Full transcript with [timestamp] format
            
        Returns:
            List of chapter dictionaries with timestamp and title
        """
        print("Analyzing transcript structure...")
        chunks = self.chunk_transcript(transcript)
        print(f"Split into {len(chunks)} overlapping segments")
        
        all_chapters = []
        
        for i, chunk in enumerate(chunks):
            print(f"\n[{i+1}/{len(chunks)}] Processing segment starting at [{chunk['start_timestamp']}]...")
            
            # Generate chapters for this chunk
            chapters = self.generate_chapters_for_chunk(chunk, i, len(chunks))
            
            if chapters:
                print(f"  → Found {len(chapters)} chapter(s)")
                for ch in chapters:
                    print(f"     [{ch['timestamp']}] {ch['title']}")
            else:
                print(f"  → No major chapters in this segment")
            
            # Add to running list
            all_chapters.extend(chapters)
            self.previous_chapters.extend(chapters)
            
            # Update context summary for next chunk (skip for last chunk)
            if i < len(chunks) - 1:
                self.context_summary = self.generate_context_summary(chunk['text'])
        
        # Sort by timestamp and deduplicate
        print("\n" + "="*60)
        print("Post-processing chapters...")
        all_chapters.sort(key=lambda x: x['timestamp_seconds'])
        final_chapters = self.deduplicate_chapters(all_chapters)
        
        print(f"✓ Generated {len(final_chapters)} final chapters")
        return final_chapters
    
    def format_chapters(self, chapters: List[Dict]) -> str:
        """Format chapters for YouTube description."""
        output = []
        for chapter in chapters:
            output.append(f"{chapter['timestamp']} {chapter['title']}")
        return '\n'.join(output)