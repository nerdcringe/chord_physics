import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import PyQt5
from scipy import signal
import pyformulas as pf
from pygame.sndarray import make_sound

matplotlib.use("Qt5agg")

from theory import *

# Define music notes
SAMPLE_RATE = 44100
DURATION = 250  # milliseconds
MAX_AMPLITUDE = 32767.0


def get_sample_times(duration_ms=DURATION):
    return np.linspace(0, duration_ms / 1000, int(SAMPLE_RATE * duration_ms / 1000), False)


def generate_note(freq_hz, duration_ms, wave_type):
    print(freq_hz)
    t = get_sample_times(duration_ms)
    MAX_NOTES_AT_ONCE = 4  # must divide amplitude by this much to prevent distortion
    if wave_type == 'square':
        wave = signal.square(2 * np.pi * freq_hz * t) * 0.3

    elif wave_type == 'sawtooth':
        wave = signal.sawtooth(2 * np.pi * freq_hz * t) * 0.4
    elif wave_type == 'triangle':
        wave = signal.sawtooth(2 * np.pi * freq_hz * t, 0.5)
    else:  # defaults to sine wave
        wave = np.sin(2 * np.pi * freq_hz * t)
    wave = (wave * MAX_AMPLITUDE/MAX_NOTES_AT_ONCE).astype(np.int32)
    return wave


def get_note_freq(n):
    return 440 * math.pow(2, (n-48)/12)


def get_chord_freqs(root_num, steps):
    freqs = []
    for step in steps:
        freqs.append(get_note_freq(root_num + step))
    return freqs


def play_chord(freqs, waveform):
    waves = []
    for f in freqs:
        waves.append(generate_note(f, DURATION, waveform))
    chord_wave = sum(waves)
    stereo_chord = np.column_stack((chord_wave, chord_wave))
    make_sound(stereo_chord).play()
    return chord_wave


plt.ion()
fig, (ax1, ax2) = plt.subplots(1, 2)
line1, = ax1.plot(0, 0, 'r-')  # Returns a tuple of line objects, thus the comma
line2, = ax2.plot(0, 0, 'r-')  # Returns a tuple of line objects, thus the comma
plt.draw()


def plot(ts, ys, title, time_samples):
    fig.suptitle(title)
    ax1.clear()
    ax1.plot(ts[:time_samples], ys[:time_samples])

    fourier = np.fft.fft(ys)
    fourier = np.abs(fourier)
    fourier = fourier / max(fourier)
    frequency = np.fft.fftfreq(ys.shape[-1], d=(1.0/SAMPLE_RATE))
    data_start = 0
    data_end = 250
    plot_freq = frequency[data_start:data_end:1]
    plot_fourier = fourier.real[data_start:data_end:]
    ax2.clear()
    ax2.plot(plot_freq, plot_fourier)

    fig.canvas.draw_idle()
    fig.canvas.flush_events()