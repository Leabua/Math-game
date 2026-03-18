import pygame
import numpy as np
import random
from pathlib import Path
from typing import Optional
import threading

ASSETS_DIR = Path(__file__).parent / "assets"
SOUNDS_DIR = ASSETS_DIR / "sounds"
MUSIC_DIR = ASSETS_DIR / "music"

SOUNDS_DIR.mkdir(parents=True, exist_ok=True)
MUSIC_DIR.mkdir(parents=True, exist_ok=True)

pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)


class SoundGenerator:
    @staticmethod
    def generate_tone(frequency: float, duration: float, volume: float = 0.3) -> pygame.mixer.Sound:
        sample_rate = 44100
        n_samples = int(duration * sample_rate)
        
        t = np.linspace(0, duration, n_samples, False)
        
        waveform = np.sin(2 * np.pi * frequency * t)
        
        envelope = np.ones(n_samples)
        attack = min(int(sample_rate * 0.01), n_samples // 4)
        decay = min(int(sample_rate * 0.1), n_samples // 2)
        
        if attack > 0:
            envelope[:attack] = np.linspace(0, 1, attack)
        if decay > 0 and decay < n_samples:
            envelope[-decay:] = np.linspace(1, 0, decay)
        
        waveform = waveform * envelope * volume
        
        waveform = (waveform * 32767).astype(np.int16)
        
        stereo = np.column_stack((waveform, waveform))
        
        sound = pygame.mixer.Sound(array=stereo)
        return sound
    
    @staticmethod
    def generate_chime(frequencies: list, duration: float, volume: float = 0.25) -> pygame.mixer.Sound:
        sample_rate = 44100
        n_samples = int(duration * sample_rate)
        
        t = np.linspace(0, duration, n_samples, False)
        waveform = np.zeros(n_samples)
        
        for i, freq in enumerate(frequencies):
            offset = i * 0.08
            if offset < duration:
                samples_offset = int(offset * sample_rate)
                t_segment = np.linspace(0, duration - offset, n_samples - samples_offset, False)
                freq_component = np.sin(2 * np.pi * freq * t_segment)
                
                envelope = np.ones(n_samples - samples_offset)
                attack = min(int(sample_rate * 0.02), len(envelope))
                decay = min(int(sample_rate * 0.3), len(envelope))
                envelope[:attack] = np.linspace(0, 1, attack)
                envelope[-decay:] = np.linspace(1, 0, decay)
                
                freq_component = freq_component * envelope * volume / len(frequencies)
                waveform[samples_offset:] += freq_component
        
        waveform = np.clip(waveform, -1, 1)
        waveform = (waveform * 32767).astype(np.int16)
        
        stereo = np.column_stack((waveform, waveform))
        return pygame.mixer.Sound(array=stereo)
    
    @staticmethod
    def generate_noise(duration: float, volume: float = 0.1) -> pygame.mixer.Sound:
        sample_rate = 44100
        n_samples = int(duration * sample_rate)
        
        noise = np.random.uniform(-1, 1, n_samples)
        
        envelope = np.ones(n_samples)
        attack = min(int(sample_rate * 0.01), n_samples // 4)
        decay = min(int(sample_rate * 0.2), n_samples // 2)
        
        if attack > 0:
            envelope[:attack] = np.linspace(0, 1, attack)
        if decay > 0 and decay < n_samples:
            envelope[-decay:] = np.linspace(1, 0, decay)
        
        noise = noise * envelope * volume
        noise = (noise * 32767).astype(np.int16)
        
        stereo = np.column_stack((noise, noise))
        return pygame.mixer.Sound(array=stereo)
    
    @staticmethod
    def generate_fanfare(duration: float = 1.5, volume: float = 0.3) -> pygame.mixer.Sound:
        notes = [523, 659, 784, 1047, 784, 1047]
        sample_rate = 44100
        n_samples = int(duration * sample_rate)
        
        waveform = np.zeros(n_samples)
        
        for i, freq in enumerate(notes):
            start = int(i * duration / len(notes) * sample_rate)
            end_time = duration / len(notes)
            end = min(start + int(end_time * sample_rate), n_samples)
            n_note = end - start
            
            t = np.linspace(0, end_time, n_note, False)
            
            note = np.sin(2 * np.pi * freq * t)
            
            env_len = n_note
            attack = min(int(sample_rate * 0.02), env_len // 4)
            decay = min(int(sample_rate * 0.3), env_len // 2)
            envelope = np.ones(env_len)
            envelope[:attack] = np.linspace(0, 1, attack)
            envelope[-decay:] = np.linspace(1, 0, decay)
            
            note = note * envelope * volume
            waveform[start:end] += note
        
        waveform = np.clip(waveform, -1, 1)
        waveform = (waveform * 32767).astype(np.int16)
        
        stereo = np.column_stack((waveform, waveform))
        return pygame.mixer.Sound(array=stereo)


class LofiMusicGenerator:
    @staticmethod
    def generate_lofi_track(duration: float = 30, seed: Optional[int] = None) -> pygame.mixer.Sound:
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
        
        sample_rate = 44100
        n_samples = int(duration * sample_rate)
        
        waveform = np.zeros(n_samples)
        
        bpm = random.choice([70, 75, 80, 85])
        beat_duration = 60 / bpm
        samples_per_beat = int(beat_duration * sample_rate)
        
        melody_notes = [261, 293, 329, 349, 392, 440, 493, 523, 587, 659, 698, 784]
        chord_notes = [
            [261, 329, 392],
            [293, 349, 440],
            [246, 293, 370],
            [220, 261, 329],
        ]
        
        vinyl_cracle_prob = 0.0001
        for i in range(n_samples):
            if np.random.random() < vinyl_cracle_prob:
                waveform[i] = np.random.uniform(-0.02, 0.02)
        
        for beat in range(n_samples // samples_per_beat):
            beat_start = beat * samples_per_beat
            
            chord = random.choice(chord_notes)
            chord_duration = beat_duration * 4
            chord_samples = int(chord_duration * sample_rate)
            
            t_chord = np.linspace(0, chord_duration, chord_samples, False)
            chord_wave = np.zeros(chord_samples)
            
            for note in chord:
                note_freq = note * 0.5
                note_wave = np.sin(2 * np.pi * note_freq * t_chord) * 0.15
                chord_wave += note_wave
            
            fade_samples = int(sample_rate * 0.1)
            chord_envelope = np.ones(chord_samples)
            chord_envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
            chord_envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
            chord_wave *= chord_envelope
            
            end_idx = min(beat_start + chord_samples, n_samples)
            waveform[beat_start:end_idx] += chord_wave[:end_idx - beat_start]
            
            if beat % random.choice([2, 4]) == 0:
                melody_note = random.choice(melody_notes)
                melody_duration = beat_duration * random.choice([0.5, 1, 2])
                melody_samples = int(melody_duration * sample_rate)
                t_melody = np.linspace(0, melody_duration, melody_samples, False)
                
                melody_wave = np.sin(2 * np.pi * melody_note * t_melody) * 0.2
                
                melody_envelope = np.ones(melody_samples)
                attack = min(int(sample_rate * 0.05), melody_samples // 4)
                decay = min(int(sample_rate * 0.4), melody_samples // 2)
                melody_envelope[:attack] = np.linspace(0, 1, attack)
                melody_envelope[-decay:] = np.linspace(1, 0, decay)
                melody_wave *= melody_envelope
                
                melody_offset = beat_start + samples_per_beat // 4
                melody_end = min(melody_offset + melody_samples, n_samples)
                waveform[melody_offset:melody_end] += melody_wave[:melody_end - melody_offset]
            
            if beat % random.choice([4, 8]) == 0:
                kick_freq = 60
                kick_duration = beat_duration * 0.5
                kick_samples = int(kick_duration * sample_rate)
                t_kick = np.linspace(0, kick_duration, kick_samples, False)
                
                kick_wave = np.sin(2 * np.pi * kick_freq * t_kick) * np.exp(-t_kick * 10)
                
                kick_envelope = np.ones(kick_samples)
                kick_attack = min(int(sample_rate * 0.01), kick_samples // 2)
                kick_envelope[:kick_attack] = np.linspace(0, 1, kick_attack)
                kick_wave *= kick_envelope * 0.3
                
                kick_end = min(beat_start + kick_samples, n_samples)
                waveform[beat_start:kick_end] += kick_wave[:kick_end - beat_start]
        
        waveform = np.clip(waveform, -0.95, 0.95)
        
        waveform = (waveform * 32767 * 0.7).astype(np.int16)
        
        stereo = np.column_stack((waveform, waveform))
        
        return pygame.mixer.Sound(array=stereo)


class SoundManager:
    def __init__(self):
        self.enabled = True
        self.music_enabled = True
        self.sounds_enabled = True
        self.volume = 0.7
        self.music_volume = 0.4
        
        self._generate_sounds()
        
        self._current_music: Optional[pygame.mixer.Sound] = None
        self._music_position = 0
        self._music_lock = threading.Lock()
        
        self._fade_thread: Optional[threading.Thread] = None
    
    def _generate_sounds(self):
        self.sounds = {}
        
        self.sounds["correct"] = SoundGenerator.generate_chime(
            [523, 659, 784], 0.4, 0.25
        )
        
        self.sounds["wrong"] = SoundGenerator.generate_tone(150, 0.3, 0.2)
        
        self.sounds["select"] = SoundGenerator.generate_tone(880, 0.08, 0.15)
        
        self.sounds["perfect"] = SoundGenerator.generate_fanfare(1.2, 0.3)
        
        self.sounds["streak"] = SoundGenerator.generate_chime(
            [440, 554, 659, 880], 0.6, 0.25
        )
    
    def _generate_music(self) -> pygame.mixer.Sound:
        seed = random.randint(0, 999999)
        duration = random.uniform(25, 35)
        return LofiMusicGenerator.generate_lofi_track(duration, seed)
    
    def play_sound(self, name: str):
        if not self.enabled or not self.sounds_enabled:
            return
        if name in self.sounds:
            self.sounds[name].set_volume(self.volume * 0.8)
            self.sounds[name].play()
    
    def start_music(self):
        if not self.enabled or not self.music_enabled:
            return
        
        with self._music_lock:
            if self._current_music:
                self._current_music.stop()
            
            self._current_music = self._generate_music()
            self._current_music.set_volume(0)
            self._current_music.play(-1)
            
            self._fade_in()
    
    def _fade_in(self):
        if not self._current_music:
            return
        
        steps = 20
        delay = 0.05
        volume_step = self.music_volume / steps
        
        def fade():
            for _ in range(steps):
                if self._current_music:
                    current = self._current_music.get_volume()
                    self._current_music.set_volume(min(current + volume_step, self.music_volume))
                pygame.time.wait(int(delay * 1000))
        
        threading.Thread(target=fade, daemon=True).start()
    
    def stop_music(self, fade_out: bool = True):
        if not self._current_music:
            return
        
        if fade_out:
            self._fade_out_and_stop()
        else:
            with self._music_lock:
                if self._current_music:
                    self._current_music.stop()
                    self._current_music = None
    
    def _fade_out_and_stop(self):
        if not self._current_music:
            return
        
        steps = 10
        delay = 0.1
        volume_step = self._current_music.get_volume() / steps
        
        def fade():
            for _ in range(steps):
                with self._music_lock:
                    if self._current_music:
                        current = self._current_music.get_volume()
                        if current > 0.01:
                            self._current_music.set_volume(max(current - volume_step, 0))
                        else:
                            self._current_music.stop()
                            self._current_music = None
                pygame.time.wait(int(delay * 1000))
        
        threading.Thread(target=fade, daemon=True).start()
    
    def set_enabled(self, enabled: bool):
        self.enabled = enabled
        if not enabled:
            self.stop_music()
    
    def set_music_enabled(self, enabled: bool):
        self.music_enabled = enabled
        if not enabled:
            self.stop_music()
        elif enabled and not self._current_music:
            self.start_music()
    
    def set_sounds_enabled(self, enabled: bool):
        self.sounds_enabled = enabled
    
    def set_volume(self, volume: float):
        self.volume = max(0, min(1, volume))
        if self._current_music:
            self._current_music.set_volume(self.music_volume)
    
    def set_music_volume(self, volume: float):
        self.music_volume = max(0, min(1, volume))
        if self._current_music:
            self._current_music.set_volume(self.music_volume)
