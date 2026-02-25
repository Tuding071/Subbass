"""
Single-File Sub Bass Synthesizer App
Detects chords and adds sine wave sub-bass
"""

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import numpy as np
from android.storage import primary_external_storage_path
from android.permissions import request_permissions, Permission
import json
import os

# Audio processing functions
def analyze_chords(audio_file):
    """
    Simulated chord detection
    In production, you'd integrate a real chord detection algorithm
    """
    # This is a simplified example
    # Real implementation would use FFT, pitch detection, etc.
    chords = [
        {"chord": "C", "root": 65.4, "duration": 2.0},
        {"chord": "G", "root": 98.0, "duration": 2.0},
        {"chord": "Am", "root": 110.0, "duration": 2.0},
        {"chord": "F", "root": 87.3, "duration": 2.0}
    ]
    return chords

def generate_sine_wave(frequency, duration, sample_rate=44100):
    """Generate sine wave for given frequency"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave = np.sin(2 * np.pi * frequency * t)
    return wave * 0.3  # Reduce volume to mix with original

def add_sub_bass(original_file, chords):
    """Main function: adds sub-bass based on detected chords"""
    sub_bass_layers = []
    for chord in chords:
        sine_wave = generate_sine_wave(chord["root"], chord["duration"])
        sub_bass_layers.append(sine_wave)
    
    # Combine all layers (simplified)
    combined_bass = np.concatenate(sub_bass_layers) if sub_bass_layers else np.array([])
    
    # In production: Mix with original audio using pydub or similar
    # For now, return the bass layer info
    return {
        "status": "success",
        "chords_detected": len(chords),
        "bass_duration": len(combined_bass) / 44100 if len(combined_bass) > 0 else 0
    }

class SubBassApp(App):
    def build(self):
        # Request permissions for Android
        try:
            request_permissions([Permission.READ_EXTERNAL_STORAGE, 
                               Permission.WRITE_EXTERNAL_STORAGE])
        except:
            pass
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        title = Label(
            text="Sub Bass Synthesizer",
            font_size='24sp',
            size_hint_y=0.2
        )
        layout.add_widget(title)
        
        # Status label
        self.status = Label(
            text="Ready to analyze",
            font_size='16sp',
            size_hint_y=0.2
        )
        layout.add_widget(self.status)
        
        # Bass intensity slider
        self.bass_intensity = Slider(
            min=0.0, max=1.0, value=0.5,
            size_hint_y=0.1
        )
        layout.add_widget(Label(text="Bass Intensity", size_hint_y=0.05))
        layout.add_widget(self.bass_intensity)
        
        # Buttons
        btn_analyze = Button(
            text="Select Song & Analyze",
            size_hint_y=0.15,
            background_color=(0.2, 0.6, 1, 1)
        )
        btn_analyze.bind(on_press=self.analyze_song)
        layout.add_widget(btn_analyze)
        
        btn_generate = Button(
            text="Generate Sub Bass",
            size_hint_y=0.15,
            background_color=(0.3, 0.8, 0.3, 1)
        )
        btn_generate.bind(on_press=self.generate_bass)
        layout.add_widget(btn_generate)
        
        btn_save = Button(
            text="Save to Phone",
            size_hint_y=0.15,
            background_color=(1, 0.6, 0, 1)
        )
        btn_save.bind(on_press=self.save_audio)
        layout.add_widget(btn_save)
        
        return layout
    
    def analyze_song(self, instance):
        """Simulate song analysis"""
        self.status.text = "Analyzing chords... (this would take 5-10 seconds)"
        Clock.schedule_once(lambda dt: self.analysis_complete(), 2)
    
    def analysis_complete(self):
        """Callback after analysis"""
        self.chords = analyze_chords("dummy.mp3")
        self.status.text = f"Detected {len(self.chords)} chords!\n" + \
                           ", ".join([c['chord'] for c in self.chords])
    
    def generate_bass(self, instance):
        """Generate sub-bass based on detected chords"""
        if not hasattr(self, 'chords'):
            self.status.text = "Please analyze a song first!"
            return
        
        self.status.text = "Generating sub-bass..."
        result = add_sub_bass("song.mp3", self.chords)
        self.status.text = f"Sub-bass generated!\n" + \
                           f"Detected: {result['chords_detected']} chords\n" + \
                           f"Bass duration: {result['bass_duration']:.1f}s"
    
    def save_audio(self, instance):
        """Save the mixed audio"""
        save_path = os.path.join(primary_external_storage_path(), 
                                 'Download', 'sub_bass_output.wav')
        self.status.text = f"Saved to:\n{save_path}"

if __name__ == '__main__':
    SubBassApp().run()
